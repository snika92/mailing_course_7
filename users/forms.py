from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm, UserChangeForm,
                                       UserCreationForm)
from phonenumber_field.formfields import PhoneNumberField

from mailing.forms import StyleFormMixin

from .models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    phone_number = PhoneNumberField(
        region="RU",
        required=False,
        help_text="Необязательное поле. Введите ваш номер телефона.",
        label="Телефон",
    )
    username = forms.CharField(max_length=50, required=True, label="Имя пользователя")
    usable_password = None

    class Meta(UserCreationForm):
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "password1",
            "password2",
        )


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    pass


class UserUpdateForm(StyleFormMixin, UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ("email", "phone_number", "avatar", "country")


class UserForgotPasswordForm(PasswordResetForm):
    """
    Запрос на восстановление пароля
    """

    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите Email",
                "autocomplete": "email",
            }
        ),
    )


class UserSetNewPasswordForm(SetPasswordForm):
    """
    Изменение пароля пользователя после подтверждения
    """

    error_messages = {"password_mismatch": "Пароли не совпадают"}
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите новый пароль",
                "autocomplete": "new-password",
            }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Подтверждение нового пароля",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Подтвердите новый пароль",
                "autocomplete": "new-password",
            }
        ),
    )
