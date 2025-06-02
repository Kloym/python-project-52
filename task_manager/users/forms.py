from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.models import User
import re


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="Подтверждение пароля"
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "username": "Имя пользователя",
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise ValidationError("Имя пользователя обязательно")
        if len(username) > 150:
            raise ValidationError("Имя пользователя не должно превышать 150 символов")
        if not re.match(r"^[\w.@+-]+$", username):
            raise ValidationError("Имя пользователя содержит недопустимые символы")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким именем уже существует")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                self.add_error("password2", "Пароли не совпадают")
            if len(password1) < 3:
                self.add_error(
                    "password1", "Ваш пароль должен содержать как минимум 3 символа"
                )
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        user.set_password(password)
        if commit:
            user.save()
        return user
