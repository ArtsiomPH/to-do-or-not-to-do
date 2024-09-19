from dataclasses import dataclass
from typing import final

import orjson
import requests
from pydantic import BaseModel
from pydantic import Extra


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


@final
@dataclass
class Client:
    host: str
    session: requests.Session

    class ApiError(RuntimeError):
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

    def api_request(self, headers: dict | None = None) -> requests.Response:
        response = self.session.get(f"{self.host}/api/", headers=headers)
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
