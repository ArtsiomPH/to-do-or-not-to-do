from typing import Any

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenVerifySerializer

from todo.models import Task
from todo.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
        )


class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict) -> User:
        req_username = validated_data["username"]
        username = req_username.replace(" ", "")
        password = validated_data["password"]
        password2 = validated_data["password2"]
        errors = {}

        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            errors["username"] = "Username already taken"

        try:
            validate_password(password)
        except ValidationError as exc:
            errors["password"] = f"Password not valid: {exc.messages}"

        if password != password2:
            errors["password2"] = "Passwords are not equal"

        if errors:
            raise serializers.ValidationError(errors)

        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["description", "title", "status", "user"]


class CustomTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs: Any) -> dict:
        response: dict = super().validate(attrs)
        if response == {}:
            return {"code": "token_is_valid"}
        return response
