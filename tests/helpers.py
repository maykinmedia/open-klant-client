import json
import logging
import os
import re
import subprocess
import time
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urljoin

import requests

from openklant_client.client import OpenKlantClient

BASE_DIR = Path(__file__).parent.parent.resolve()
COMPOSE_PATH = BASE_DIR / "docker-compose.yaml"

# The klantinteracties API version served by the image pinned in docker-compose.yaml.
# Bump this together with the image tag; tests/test_cassettes.py enforces that the
# recorded cassettes agree with it.
OPEN_KLANT_API_VERSION = "0.8.0"

_IMAGE_TAG_RE = re.compile(
    r"maykinmedia/open-klant:\$\{OPEN_KLANT_IMAGE_TAG:-(?P<tag>[^}]+)\}"
)

logger = logging.getLogger(__name__)


def _pinned_image_tag() -> str:
    """Read the pinned Open Klant image tag from the docker-compose default.

    docker-compose.yaml is the single source of truth for the version the
    testsuite records against. Refuse to run if the pin has been removed.
    """
    match = _IMAGE_TAG_RE.search(COMPOSE_PATH.read_text())
    if match is None:
        raise RuntimeError(
            f"No pinned Open Klant image tag found in {COMPOSE_PATH}. The testsuite "
            f"refuses to run against an unpinned image, because the VCR cassettes in "
            f"tests/cassettes are only valid for one specific version."
        )
    return match.group("tag")


OPEN_KLANT_IMAGE_TAG = _pinned_image_tag()


class OpenKlantServiceManager:
    _in_server_context: bool = False
    _django_service_name: str = "web"
    _api_root: str = "http://localhost:8338"
    _api_path: str = "/klantinteracties/api/v1"
    _api_token: str = "b2eb1da9861da88743d72a3fb4344288fe2cba44"
    _docker_compose_project_name: str = "openklant-api-test"
    _docker_compose_path: Path = COMPOSE_PATH

    def _docker_compose(
        self,
        *args: str,
        check: bool = True,
        input: str | None = None,
    ):
        input_data = {"text": True, "input": input} if input else {}
        try:
            return subprocess.run(
                args=[
                    "docker",
                    "compose",
                    "-f",
                    str(self._docker_compose_path),
                    "-p",
                    self._docker_compose_project_name,
                    *args,
                ],
                check=check,
                capture_output=True,
                # Pass the pin explicitly so an ambient OPEN_KLANT_IMAGE_TAG in the
                # caller's environment cannot silently change what we record against.
                env={**os.environ, "OPEN_KLANT_IMAGE_TAG": OPEN_KLANT_IMAGE_TAG},
                **input_data,
            )
        except subprocess.CalledProcessError as exc:
            logger.exception(
                "Unable to execute command. stderr: %s, stdout: %s",
                exc.stderr,
                exc.stdout,
            )
            raise

    def _manage_py(
        self,
        *args: str,
        input: str | None = None,
    ):
        self._docker_compose(
            "run",
            "--rm",
            self._django_service_name,
            "python",
            "src/manage.py",
            *args,
            input=input,
        )

    def _service_teardown(self):
        self._docker_compose("kill", check=False)
        self._docker_compose("down", "-v")
        self._docker_compose("rm", "-f")

    def _service_init(self):
        self._docker_compose("up", "-d")
        self._wait_for_response()
        self._manage_py("migrate")

    def reset_db_state(self):
        self._manage_py("flush", "--no-input")
        self._load_fixture_from_json_string(self._generate_token_fixture())

    def _load_fixture_from_json_string(self, fixture: str):
        self._manage_py(
            "loaddata",
            "--format",
            "json",
            "-",  # i.e. stdin
            input=fixture,
        )

    def _generate_token_fixture(self):
        return json.dumps(
            [
                {
                    "model": "token.tokenauth",
                    "pk": 1,
                    "fields": {
                        "identifier": "test-token",
                        "token": self._api_token,
                        "contact_person": "Boaty McBoatface",
                        "email": "boaty@mcboatface.com",
                        "organization": "",
                        "last_modified": "2024-08-22T07:43:21.837Z",
                        "created": "2024-08-22T07:43:21.837Z",
                        "application": "",
                        "administration": "",
                    },
                },
                # add admin user for convenience + debugging
                {
                    "model": "accounts.user",
                    "pk": 1,
                    "fields": {
                        # password is "secret"
                        "password": (
                            "pbkdf2_sha256$600000$11HRNvD3J8QPTCkp0avgKX$"
                            "gY/NX5+Ap8jAmD86HxEneVHwzi9+g45NhTBMkB3vJuo="
                        ),
                        "last_login": "2025-01-28T10:30:23.474Z",
                        "is_superuser": True,
                        "username": "admin",
                        "first_name": "",
                        "last_name": "",
                        "email": "admin@oip.nl",
                        "is_staff": True,
                        "is_active": True,
                        "date_joined": "2025-01-28T10:29:59.843Z",
                        "groups": [],
                        "user_permissions": [],
                    },
                },
            ]
        )

    def _wait_for_response(self, interval=0.5, max_wait=60):
        start_time = time.time()
        while True:
            try:
                response = requests.get(self._api_root)
                return response
            except requests.RequestException:
                logger.debug("Exception while checking for liveness", exc_info=True)
                elapsed_time = time.time() - start_time
                if elapsed_time > max_wait:
                    logger.info("Max wait time exceeded.")
                    raise RuntimeError(
                        f"Maximum wait for service to be healthy exceeded: "
                        f"{elapsed_time} > {max_wait}"
                    ) from None

                time.sleep(interval)

    def setUp(self):
        if self._in_server_context:
            raise RuntimeError(
                "You cannot have multiple server contexts active at the same time"
            )

        self._in_server_context = True
        self._service_teardown()
        self._service_init()

    def tearDown(self):
        self._service_teardown()
        self._in_server_context = False

    @property
    def api_url(self):
        return urljoin(self._api_root, self._api_path)

    def client_factory(self):
        return OpenKlantClient(
            base_url=self.api_url,
            token=self._api_token,
        )

    def clean_state(self):
        """Yield a client configured to talk a live OpenKlant service.

        Note that this requires the live server to have been spawned,
        either imperatively:

            service.setUp()
            with service.clean_state() as client:
                client.do_stuff()

            service.tearDown()

        ... or using the live_service() context manager:

            with service.live_server_manager() as live_service:
                with live_service.clean_state() as client:
                    client.do_something()

        """
        if not self._in_server_context:
            raise RuntimeError(
                "You must execute this context within the server context"
            )

        @contextmanager
        def clean_state_manager(*args, **kwds):
            self.reset_db_state()
            yield self.client_factory()

        return clean_state_manager()

    def live_service(self):
        """Context manager to spawn a live OpenKlant service and clean it up.

        You will commonly nest a clean_state() context manager within the
        live_service block, for instance:

            with service.live_server_manager() as live_service:
                with live_service.clean_state() as client:
                    client.do_something()
        """

        @contextmanager
        def live_server_manager(*args, **kwds):
            try:
                self.setUp()
                yield self
            finally:
                self.tearDown()

        return live_server_manager()


class LiveOpenKlantTestMixin:
    _service: OpenKlantServiceManager
    use_live_service: bool = False

    @classmethod
    def should_bypass_live_server(cls) -> bool:
        return cls.use_live_service

    @property
    def openklant_client(self) -> OpenKlantClient:
        return self._service.client_factory()

    def reset_db(self):
        if not self.should_bypass_live_server():
            self._service.reset_db_state()

    @classmethod
    def setUpClass(cls):
        cls._service = OpenKlantServiceManager()

        if not cls.should_bypass_live_server():
            cls._service.setUp()

    @classmethod
    def tearDownClass(cls) -> None:
        if not cls.should_bypass_live_server():
            cls._service.tearDown()

    def setUp(self):
        self.reset_db()
