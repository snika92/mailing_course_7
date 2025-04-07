from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig

from .views import (BlockUserView, CustomLoginView, RegisterView,
                    UserDetailView, UserForgotPasswordView, UserListView,
                    UserPasswordResetConfirmView, UserUpdateViews,
                    email_verification)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("users/", UserListView.as_view(), name="users_list"),
    path("users/<int:pk>/block_user", BlockUserView.as_view(), name="block_user"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_details"),
    path("users/<int:pk>/update", UserUpdateViews.as_view(), name="user_update"),
    path("password-reset/", UserForgotPasswordView.as_view(), name="password-reset"),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
]
