from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import (
    UserCreationForm,
)


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                "label": _("Пароль"),
                "placeholder": _("Пароль"),
                "class": "form-control",
            }
        ),
        help_text=_("Ваш пароль должен содержать как минимум 3 символа."),
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={
                "label": _("Подтверждение пароля"),
                "placeholder": _("Подтверждение пароля"),
                "class": "form-control",
            }
        ),
        help_text=_("Для подтверждения введите, пожалуйста, пароль ещё раз."),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password1", "password2")

        labels = {
            "first_name": _("Имя"),
            "last_name": _("Фамилия"),
            "username": _("Имя пользователя"),
        }

        help_texts = {
            "username": _(
                """Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_."""
            ),
        }
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": _("Имя пользователя"),
                    "class": "form-control",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": _("Имя"),
                    "class": "form-control",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": _("Фамилия"),
                    "class": "form-control",
                }
            ),
        }

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if password1 and len(password1) < 3:
            raise forms.ValidationError(
                _("""Ваш пароль должен содержать как минимум 3 символа.""")
            )
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Пароли не совпадают"))
        return cleaned_data

    def _post_clean(self):
        super(forms.ModelForm, self)._post_clean()
