from dataclasses import dataclass
from typing import final

import orjson
import requests
from pydantic import BaseModel
from pydantic import Extra
from pydantic import Field

from todo.models import User


class MyModel(BaseModel):
    class Meta:
        extra = Extra.forbid
        json_dumps = orjson.dumps
        json_loads = orjson.loads
        orm_mode = True
        validate_assignment = True


class Authority(MyModel):
    username: str
    first_name: str
    last_name: str


class RegisterResponse(MyModel):
    message: str
    user: Authority


class TokenPairResponse(MyModel):
    access: str
    refresh: str


class AccessTokenResponse(MyModel):
    access: str


class VerifyTokenResponse(MyModel):
    code: str


class TaskResponse(MyModel):
    task_id: int = Field(..., alias="id")
    title: str
    description: str | None
    status: str
    user_id: int = Field(..., alias="user")


class TasksListResponse(MyModel):
    count: int
    nxt: int | None = Field(None, alias="next")
    previous: int | None
    results: list[TaskResponse]


@final
@dataclass
class Client:
    host: str
    session: requests.Session
    token: str | None = None

    @property
    def headers(self) -> dict[str, str]:
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        return headers

    class ApiError(Exception):
        def __init__(
            self,
            *args: tuple,
            message: str,
            http_code: int,
        ):
            super().__init__(*args)
            self.message = message
            self.http_code = http_code

        def __str__(self) -> str:
            return f"message:{self.message}, http_code:{self.http_code}"

    def api_request(self) -> requests.Response:
        response = self.session.get(f"{self.host}/api/", headers=self.headers)
        return response

    def register(
        self,
        *,
        password: str,
        username: str,
    ) -> RegisterResponse:
        response = self.session.post(
            f"{self.host}/api/signup/",
            data=orjson.dumps(
                {
                    "username": username,
                    "password": password,
                    "password2": password,
                }
            ),
        )
        if not response.ok:
            raise self.ApiError(
                message=response.json(),
                http_code=response.status_code,
            )
        payload = RegisterResponse.model_validate_json(response.text)
        return payload

    def authenticate(
        self, *, username: str, password: str
    ) -> TokenPairResponse:
        response = self.session.post(
            f"{self.host}/api/signin/",
            data=orjson.dumps(
                {
                    "username": username,
                    "password": password,
                }
            ),
        )
        if not response.ok:
            raise self.ApiError(
                message=response.json(),
                http_code=response.status_code,
            )
        payload = TokenPairResponse.model_validate_json(response.text)
        return payload

    def get_refresh_token(
        self,
        *,
        username: str,
        password: str,
    ) -> str:
        response = self.authenticate(username=username, password=password)
        assert response.access
        assert response.refresh

        return response.refresh

    def get_new_access_token(
        self,
        refresh_token: str,
    ) -> AccessTokenResponse:
        response = self.session.post(
            f"{self.host}/api/token/refresh/",
            data=orjson.dumps(
                {
                    "refresh": refresh_token,
                }
            ),
        )
        if not response.ok:
            raise self.ApiError(
                message=response.json(),
                http_code=response.status_code,
            )
        payload = AccessTokenResponse.model_validate_json(response.text)
        return payload

    def verify_token(self, refresh_token: str) -> VerifyTokenResponse:
        response = self.session.post(
            f"{self.host}/api/token/verify/",
            data=orjson.dumps(
                {
                    "token": refresh_token,
                }
            ),
        )
        if not response.ok:
            raise self.ApiError(
                message=response.json(),
                http_code=response.status_code,
            )
        payload = VerifyTokenResponse.model_validate_json(response.text)
        return payload

    def create_task(
        self,
        *,
        title: str,
        description: str | None,
        user: User,
        status: str = "new",
    ) -> TaskResponse:
        response = self.session.post(
            f"{self.host}/api/tasks/",
            data=orjson.dumps(
                {
                    "title": title,
                    "description": description,
                    "user": user.id,
                    "status": status,
                }
            ),
            headers=self.headers,
        )
        if not response.ok:
            raise self.ApiError(
                message=response.json(),
                http_code=response.status_code,
            )
        payload = TaskResponse.model_validate_json(response.text)
        return payload

    def get_all_tasks(self) -> list[TaskResponse]:
        response = self.session.get(
            f"{self.host}/api/tasks/", headers=self.headers
        )
        if not response.ok:
            raise self.ApiError(
                message=response.json(),
                http_code=response.status_code,
            )
        payload = TasksListResponse.model_validate_json(response.text)
        tasks_list = payload.results
        return tasks_list

    def retrieve_task(self, task_id: int) -> TaskResponse:
        response = self.session.get(
            f"{self.host}/api/tasks/{task_id}/", headers=self.headers
        )
        if not response.ok:
            raise self.ApiError(
                message=response.json(),
                http_code=response.status_code,
            )
        payload = TaskResponse.model_validate_json(response.text)
        return payload

    def update_task(
        self,
        task_id: int | None,
        *,
        title: str,
        description: str | None = None,
        status: str | None = None,
    ) -> TaskResponse:
        for_update = {
            key: value
            for key, value in {
                "title": title,
                "description": description,
                "status": status,
            }.items()
            if value is not None
        }
        response = self.session.patch(
            f"{self.host}/api/tasks/{task_id}/",
            data=orjson.dumps(for_update),
            headers=self.headers,
        )
        if not response.ok:
            raise self.ApiError(
                message=response.json(),
                http_code=response.status_code,
            )
        payload = TaskResponse.model_validate_json(response.text)
        return payload
