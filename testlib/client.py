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
        assert response.ok, response.text
        payload = RegisterResponse.model_validate_json(response.text)
        return payload
