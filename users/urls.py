from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig

from .views import CustomLoginView, RegisterView, email_verification

app_name = UsersConfig.name

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
]
