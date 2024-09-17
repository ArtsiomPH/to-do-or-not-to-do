from typing import Iterable

import pytest
import requests
from faker import Faker

from testlib.client import Client

DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "Agent/007",
}

DEFAULT_HOST = "localhost"

fake = Faker()


@pytest.fixture(scope="function")
def client() -> Iterable[Client]:
    with requests.Session() as session:
        session.headers.update(DEFAULT_HEADERS)
        yield Client(host=f"http://{DEFAULT_HOST}:8000", session=session)


@pytest.fixture(scope="function")
def random_username() -> Iterable[str]:
    username = fake.user_name()
    yield username
