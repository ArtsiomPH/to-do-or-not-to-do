from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from todo.helpers.classes import WithOwnerType


class IsOwnerOrReadOnly(BasePermission):
    message = "Only owners can change and delete objects"

    def has_object_permission(
        self, request: Request, view: APIView, obj: WithOwnerType
    ) -> bool:
        if request.method in SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user
