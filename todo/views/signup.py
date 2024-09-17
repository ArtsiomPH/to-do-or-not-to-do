from rest_framework import generics
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response

from todo import serializers


class SignupView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.SignupSerializer

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "user": serializers.UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "user created successfully",
            }
        )
