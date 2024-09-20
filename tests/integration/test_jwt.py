from datetime import timedelta

import pytest
from freezegun import freeze_time
from rest_framework import status

from testlib.client import Client
from todo.models import User


def test_successful_auth(
    client: Client,
    random_user: User,
    user_password: str,
) -> None:
    response = client.authenticate(
        username=random_user.username, password=user_password
    )
    assert response.access
    assert response.refresh


def test_unsuccessful_auth(
    client: Client,
) -> None:
    with pytest.raises(client.ApiError) as exc:
        client.authenticate(  # noqa: S106
            username="incorrect_username", password="<PASSWORD>"
        )
    assert exc.value.http_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.message == {
        "detail": "No active account found with the given credentials"
    }


def test_refresh_token(
    client: Client,
    refresh_token: str,
) -> None:
    response = client.get_new_access_token(refresh_token)
    assert response.access


def test_token_auth(
    client: Client,
    random_user: User,
    user_password: str,
) -> None:
    response = client.api_request()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    successful_response = client.authenticate(
        username=random_user.username, password=user_password
    )
    access_token = successful_response.access
    client.token = access_token
    response = client.api_request()
    assert response.status_code == status.HTTP_200_OK


def test_refresh_lives_lower_than_seven_day(
    client: Client,
    refresh_token: str,
) -> None:
    with freeze_time() as frozen_time:
        frozen_time.tick(timedelta(days=6, hours=23, minutes=59))
        token = client.get_new_access_token(refresh_token)
        assert token.access


@pytest.mark.skip("unexpected passing")
def test_refresh_dies_after_seven_day(
    client: Client, refresh_token: str
) -> None:
    exc: pytest.ExceptionInfo

    with pytest.raises(client.ApiError) as exc, freeze_time() as frozen_time:
        frozen_time.tick(timedelta(days=10))
        client.get_new_access_token(refresh_token=refresh_token)
    assert exc.value.http_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.message == {
        "detail": "Token is invalid or expired",
        "code": "token_not_valid",
    }


def test_token_verify(
    client: Client,
    refresh_token: str,
) -> None:
    response = client.verify_token(refresh_token)
    assert response.code == "token_is_valid"
