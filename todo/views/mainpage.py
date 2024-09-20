from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response


class MainPageView(GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request) -> Response:
        return Response({"message": "Hello"})
