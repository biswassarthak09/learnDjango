from django.urls import path
from . import views
from .serializer import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("register/", views.register_user, name = "register_user"),
    path("login/", views.login_user, name = "login"),
    path("logout/", views.logout_user, name = "logout"),
    path("token/", MyTokenObtainPairView.as_view(), name = "token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login_jwt/", views.login_user_with_jwt, name = "login_jwt"),
]