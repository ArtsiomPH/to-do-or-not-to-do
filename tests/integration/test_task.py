from testlib.client import Client
from todo.models import Task
from todo.models import User


def test_task_create(
    client: Client,
    random_user: User,
    random_user_access_token: str,
    random_task: Task,
) -> None:
    client.token = random_user_access_token
    created_task = client.create_task(
        title=random_task.title,
        description=random_task.description,
        status=random_task.status,
        user=random_user,
    )
    assert random_task.title == created_task.title
    assert random_task.description == created_task.description
    assert random_task.status == created_task.status
    assert created_task.user_id == random_user.id
