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
    response = client.refresh_token_request(refresh_token)
    assert response.access


@pytest.mark.skip("no api with permissions")
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
    headers = {"Authorization": "Bearer " + access_token}
    response = client.api_request(headers=headers)
    assert response.status_code == status.HTTP_200_OK


def test_refresh_lives_lower_than_one_day(
    client: Client,
    refresh_token: str,
) -> None:
    with freeze_time() as frozen_time:
        frozen_time.tick(timedelta(hours=23, minutes=59))
        response = client.refresh_token_request(refresh_token)
        assert response.access
