from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       UsernameField)
from django.forms import BooleanField
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
