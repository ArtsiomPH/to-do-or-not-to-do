from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("todo.urls")),
    path("drf/", include("rest_framework.urls")),
]
