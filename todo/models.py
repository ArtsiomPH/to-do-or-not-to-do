from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150)

    def __str__(self) -> str:
        return self.username


class Task(models.Model):
    class TaskStatus(models.TextChoices):
        NEW = "new"
        PENDING = "pending"
        DONE = "done"

    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=150)
    status = models.CharField(
        choices=TaskStatus.choices, default=TaskStatus.NEW
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
