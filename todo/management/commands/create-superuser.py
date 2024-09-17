from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """
    Create a superuser if none exist.
    Takes args from environment variables.
    """

    def handle(self, *args: Any, **options: Any) -> None:
        username = "admin"
        password = "admin1234"
        email = "admin@admin.com"

        if User.objects.filter(username=username).exists():
            self.stdout.write(f"User '{username}' exists already")
            return

        User.objects.create_superuser(
            username=username, password=password, email=email
        )

        self.stdout.write(f"Superuser '{username}' was created successfully")
