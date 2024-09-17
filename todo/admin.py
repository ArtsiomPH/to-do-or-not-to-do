from django.contrib import admin

from .models import Task
from .models import User


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "status",
        "title",
        "user",
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
    )
