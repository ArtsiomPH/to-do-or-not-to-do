import os
from typing import Iterable

import django
import pytest
import requests
from faker import Faker

if "env setting":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()

from testlib.client import Client
from todo.models import Task
from todo.models import User

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


@pytest.fixture(scope="function")
def user_password() -> Iterable[str]:
    password = fake.password(length=7)
    yield password


@pytest.fixture(scope="function")
def random_user(
    random_username: str,
    user_password: str,
) -> Iterable[User]:
    user = User.objects.create_user(
        username=random_username, password=user_password
    )
    yield user
    user.delete()


@pytest.fixture(scope="function")
def refresh_token(
    client: Client, random_user: User, user_password: str
) -> Iterable[str]:
    response = client.authenticate(
        username=random_user.username, password=user_password
    )
    token = response.refresh
    yield token


@pytest.fixture(scope="function")
def random_user_access_token(
    client: Client, random_user: User, user_password: str
) -> str:
    response = client.authenticate(
        username=random_user.username, password=user_password
    )

    access = response.access
    return access


@pytest.fixture(scope="function")
def random_task() -> Iterable[Task]:
    title = fake.word()
    description = fake.text()
    status: str = fake.random_element(elements=Task.TaskStatus.values)
    task = Task(title=title, description=description, status=status)
    yield task
