import pytest

from testlib.client import Client


@pytest.mark.parametrize(
    "password", [pytest.param("lt6", marks=pytest.mark.xfail), "good_pass"]
)
def test_signup(
    client: Client,
    password: str,
    random_username: str,
) -> None:
    expected_message = "user created successfully"
    registered = client.register(username=random_username, password=password)
    assert registered.user.username == random_username
    assert registered.message == expected_message
