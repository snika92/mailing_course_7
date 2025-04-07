import secrets

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.views import View

from config.settings import EMAIL_HOST_USER

from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm, UserForgotPasswordForm, UserSetNewPasswordForm
from .models import User


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            "Подтверждение почты",
            f"Привет! Перейди по ссылке для подтверждения почты {url}",
            EMAIL_HOST_USER,
            [user.email],
        )
        return super().form_valid(form)


def send_welcome_email(user_email):
    send_mail(
        "Добро пожаловать в менеджер рассылок!",
        f"Спасибо, что зарегистрировались!",
        EMAIL_HOST_USER,
        [user_email],
    )


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    send_welcome_email(user.email)
    return redirect(reverse("users:login"))


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = User
    template_name = "users/users_list.html"
    context_object_name = "users"
    permission_required = "users.view_user"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_superuser=False)
        queryset = queryset.exclude(groups__permissions__codename='can_block_users')
        return queryset.order_by("-is_active")


class BlockUserView(LoginRequiredMixin, View):

    def post(self, request, pk):
        user = get_object_or_404(User, id=pk)

        if not request.user.has_perm("users.can_block_users"):
            raise PermissionDenied("У вас нет права на блокировку/разблокировку пользователя")

        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True

        user.save()
        return redirect("users:users_list")


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/user_details.html"
    context_object_name = "user"


class UserUpdateViews(LoginRequiredMixin, UpdateView):
    template_name = "users/user_update.html"
    form_class = UserUpdateForm
    success_url = reverse_lazy("users:login")

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_success_url(self):
        return reverse("users:user_details", args=[self.kwargs.get("pk")])


class UserForgotPasswordView(PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """
    from_email = EMAIL_HOST_USER
    form_class = UserForgotPasswordForm
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy("users:password_reset_done")
    email_template_name = 'users/password_reset_email.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """
    form_class = UserSetNewPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy("users:password_reset_complete")
