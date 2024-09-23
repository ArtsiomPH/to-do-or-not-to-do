import pytest
from rest_framework import status

from testlib.client import Client


def test_isauthenticated_perm(client: Client) -> None:
    with pytest.raises(client.ApiError) as exc:
        client.get_all_tasks()

    assert exc.value.http_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.message == {
        "detail": "Authentication credentials were not provided."
    }
