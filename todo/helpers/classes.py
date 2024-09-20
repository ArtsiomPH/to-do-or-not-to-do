from typing import Protocol

from todo.models import User


class WithOwnerType(Protocol):
    user: User
