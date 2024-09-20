import pytest
from rest_framework import status

from testlib.client import Client
from todo.models import Task
from todo.models import User


def test_task_create(
    client: Client,
    random_user: User,
    random_user_access_token: str,
    task_model: Task,
) -> None:
    client.token = random_user_access_token
    created_task = client.create_task(
        title=task_model.title,
        description=task_model.description,
        status=task_model.status,
        user=random_user,
    )
    assert task_model.title == created_task.title
    assert task_model.description == created_task.description
    assert task_model.status == created_task.status
    assert created_task.user_id == random_user.id


def test_task_list(
    another_random_user_task: Task,
    client: Client,
    random_user: User,
    random_user_access_token: str,
    random_user_task: Task,
) -> None:
    client.token = random_user_access_token
    tasks_list = client.get_all_tasks()
    tasks_id_list = [task.task_id for task in tasks_list]
    assert len(tasks_list) > 0
    assert another_random_user_task.id in tasks_id_list
    assert random_user_task.id in tasks_id_list


def test_retrieve(
    client: Client,
    random_user: User,
    random_user_access_token: str,
    random_user_task: Task,
) -> None:
    client.token = random_user_access_token
    db_task = client.retrieve_task(random_user_task.id)
    assert db_task.title == random_user_task.title
    assert db_task.description == random_user_task.description
    assert db_task.status == random_user_task.status
    assert db_task.user_id == random_user.id


def test_update(
    client: Client,
    random_user_access_token: str,
    random_user_task: Task,
) -> None:
    client.token = random_user_access_token
    for_update = {
        "title": "new_title",
        "description": "new_description",
        "status": "pending",
    }
    updated_task = client.update_task(random_user_task.id, **for_update)
    assert updated_task.task_id == random_user_task.id
    assert updated_task.title == for_update["title"]
    assert updated_task.description == for_update["description"]
    assert updated_task.status == for_update["status"]


def test_only_owner_can_update_task(
    client: Client,
    random_user_access_token: str,
    another_random_user_access_token: str,
    random_user_task: Task,
) -> None:
    client.token = random_user_access_token
    for_update = {"title": "new_title"}
    updated_task = client.update_task(random_user_task.id, **for_update)
    assert updated_task.task_id == random_user_task.id
    assert updated_task.title == for_update["title"]

    client.token = another_random_user_access_token
    with pytest.raises(client.ApiError) as exc:
        for_update = {"title": "test_title"}
        client.update_task(random_user_task.id, **for_update)

    assert exc.value.http_code == status.HTTP_403_FORBIDDEN
    assert exc.value.message == {
        "detail": "Only owners can change and delete objects"
    }


def test_filtration(
    client: Client,
    random_user_access_token: str,
    random_user_pending_task: Task,
) -> None:
    client.token = random_user_access_token
    pending_tasks = client.get_all_tasks({"status": "pending"})
    assert all(task.status == "pending" for task in pending_tasks)
    assert random_user_pending_task.id in [
        task.task_id for task in pending_tasks
    ]


def test_mark_task_completed(
    client: Client,
    random_user_access_token: str,
    random_user_pending_task: Task,
) -> None:
    client.token = random_user_access_token
    response = client.change_task_status(
        random_user_pending_task.id, status="done"
    )
    assert response.task.task_id == random_user_pending_task.id
    assert response.task.status == "done"
    assert response.message == "task status updated"


def test_delete_task(
    another_random_user_access_token: str,
    client: Client,
    random_user_access_token: str,
    random_user_task: Task,
) -> None:
    client.token = another_random_user_access_token
    with pytest.raises(client.ApiError) as exc:
        client.delete_task(random_user_task.id)
    assert exc.value.http_code == status.HTTP_403_FORBIDDEN
    assert exc.value.message == {
        "detail": "Only owners can change and delete objects"
    }

    client.token = random_user_access_token
    client.delete_task(random_user_task.id)
    with pytest.raises(client.ApiError) as new_exc:
        client.retrieve_task(random_user_task.id)
    assert new_exc.value.http_code == status.HTTP_404_NOT_FOUND
    assert new_exc.value.message == {"detail": "Not found."}
