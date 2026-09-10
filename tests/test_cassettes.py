"""Guard against Open Klant API version drift in the recorded VCR cassettes.

The cassettes in tests/cassettes are only valid for the Open Klant version pinned
in docker-compose.yaml. Recording a subset of them against a different version
leaves the suite green while it silently asserts the behaviour of two different
servers, which is how the suite ended up mixing four API generations before.

These checks are a text scan rather than a YAML parse: the scan yields the same
counts roughly sixty times faster, and it fails loudly rather than silently if
VCR ever changes how it serializes headers.
"""

import re
from collections import Counter, defaultdict
from collections.abc import Iterable

import pytest

from tests.helpers import BASE_DIR, OPEN_KLANT_API_VERSION

CASSETTE_DIR = BASE_DIR / "tests" / "cassettes"

# A failing check usually implicates most of the suite at once, so report a sample
# rather than every offender.
MAX_REPORTED = 5

# Each recorded interaction starts a list item at column 0.
RE_INTERACTION = re.compile(r"^- request:\s*$", re.MULTILINE)

# VCR serializes response headers as a block sequence:
#
#     API-version:
#     - 0.8.0
RE_API_VERSION = re.compile(
    r"^\s*api-version:\s*\n\s*-\s*(?P<version>\S+)\s*$", re.IGNORECASE | re.MULTILINE
)


def _sample(names: Iterable[str]) -> str:
    """Render a bounded, deterministic sample of cassette names."""
    names = sorted(names)
    shown = ", ".join(names[:MAX_REPORTED])
    remainder = len(names) - MAX_REPORTED
    return f"{shown} (and {remainder} more)" if remainder > 0 else shown


@pytest.fixture(autouse=True)
def _skip_while_recording(request):
    """Skip while cassettes are being rewritten.

    regenerate_vcr_fixtures.sh deletes the cassette directory and the tests
    repopulate it as they run, so mid-recording this module would inspect a
    half-written tree. The script runs these checks again once recording has
    finished.
    """
    # pytest-recording registers --record-mode with a default of None, and treats
    # that as "none". The getoption default covers the plugin being absent.
    record_mode = request.config.getoption("--record-mode", None) or "none"
    if record_mode != "none":
        pytest.skip("cassettes are being rewritten; the guard runs after recording")


@pytest.fixture(scope="module")
def cassettes() -> dict[str, tuple[int, Counter]]:
    """Map each cassette to its interaction count and the API versions it recorded."""
    return {
        str(path.relative_to(BASE_DIR)): (
            len(RE_INTERACTION.findall(text := path.read_text())),
            Counter(match.group("version") for match in RE_API_VERSION.finditer(text)),
        )
        for path in sorted(CASSETTE_DIR.rglob("*.yaml"))
    }


def test_cassettes_are_present(cassettes) -> None:
    """Without this, an empty scan would satisfy every other check vacuously."""
    assert cassettes, f"No cassettes found in {CASSETTE_DIR}"

    empty = [name for name, (interactions, _) in cassettes.items() if not interactions]
    assert not empty, (
        f"{len(empty)} of {len(cassettes)} cassettes record no interaction at all: "
        f"{_sample(empty)}. Either these are stale, or VCR changed its serialization "
        f"and this guard can no longer read it."
    )


def test_every_interaction_declares_an_api_version(cassettes) -> None:
    """Every response should come from Open Klant, which always sets the header."""
    mismatched = {
        name: (interactions, sum(versions.values()))
        for name, (interactions, versions) in cassettes.items()
        if interactions != sum(versions.values())
    }
    detail = "; ".join(
        f"{name}: {interactions} interaction(s) but {headers} API-version header(s)"
        for name, (interactions, headers) in sorted(mismatched.items())[:MAX_REPORTED]
    )
    assert not mismatched, (
        f"{len(mismatched)} of {len(cassettes)} cassettes contain responses that "
        f"declare no API-version header: {detail}"
        f"{'; ...' if len(mismatched) > MAX_REPORTED else ''}"
    )


def test_cassettes_match_the_pinned_api_version(cassettes) -> None:
    """All cassettes must agree, and agree with the pinned Open Klant version."""
    by_version: defaultdict[str, list[str]] = defaultdict(list)
    for name, (_, versions) in cassettes.items():
        for version in set(versions) - {OPEN_KLANT_API_VERSION}:
            by_version[version].append(name)

    detail = "; ".join(
        f"{version} in {len(names)} cassette(s): {_sample(names)}"
        for version, names in sorted(by_version.items())
    )
    assert not by_version, (
        f"Cassettes recorded against an Open Klant version other than the pinned "
        f"API-version {OPEN_KLANT_API_VERSION} -- {detail}. Re-record the full suite "
        f"with ./regenerate_vcr_fixtures.sh, or, if the pin itself moved, bump both "
        f"the image tag in docker-compose.yaml and OPEN_KLANT_API_VERSION in "
        f"tests/helpers.py."
    )
