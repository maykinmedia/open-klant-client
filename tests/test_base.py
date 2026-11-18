from unittest.mock import MagicMock

import pytest

from openklant_client._resources.base import ResourceMixin


@pytest.mark.parametrize(
    "resource_method,http_verb,kwargs",
    [
        ("_get", "get", {}),
        ("_post", "post", {"data": {"foo": "bar"}}),
        ("_put", "put", {"data": {"foo": "bar"}}),
        ("_patch", "patch", {"data": {"foo": "bar"}}),
        ("_delete", "delete", {}),
        ("_options", "options", {}),
    ],
)
def test_resource_mixin_sends_expected_http_verb(resource_method, http_verb, kwargs):
    # Regression test for a bug where `_options()` erroneously sent a DELETE
    # request instead of an OPTIONS request.
    http_client = MagicMock()
    resource = ResourceMixin(http_client)

    getattr(resource, resource_method)("some-path", **kwargs)

    http_client.request.assert_called_once()
    called_verb = http_client.request.call_args.args[0]
    assert called_verb == http_verb
