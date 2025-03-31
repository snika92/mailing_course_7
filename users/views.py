import secrets

from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER

from .forms import UserLoginForm, UserRegisterForm
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
