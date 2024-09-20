from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from todo.models import Task
from todo.permissions import IsOwnerOrReadOnly
from todo.serializers import TaskSerializer
from todo.serializers import UpdateTaskStatusSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    )
    filterset_fields = [
        "status",
    ]

    @action(
        detail=True,
        methods=["PUT", "PATCH"],
        serializer_class=UpdateTaskStatusSerializer,
    )
    def update_status(self, request: Request, pk: int) -> Response:
        task = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_task = serializer.update(task, serializer.validated_data)
        response = {
            "task": TaskSerializer(updated_task).data,
            "message": "task status updated",
        }
        return Response(response)
