from django.urls import include
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from todo.views import CustomTokenVerifyView
from todo.views import MainPageView
from todo.views import SignupView
from todo.views import TaskViewSet

router = routers.DefaultRouter()
router.register(prefix="tasks", viewset=TaskViewSet, basename="task")

urlpatterns = [
    path("", include(router.urls)),
    path("", MainPageView.as_view(), name="main_page"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("signin/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "token/verify/", CustomTokenVerifyView.as_view(), name="token_verify"
    ),
]
