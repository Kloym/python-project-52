from django import forms
from django.contrib.auth.models import User
from .models import Status, Task

class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        help_text='Ваш пароль должен содержать как минимум 3 символа',
        required=False,
        min_length=3,
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput,
        help_text='Для подтверждения введите, пожалуйста, пароль ещё раз',
        required=False,
        min_length=3,
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя',
        }
        help_texts = {
            'username': 'Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.',
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError('Пароли не совпадают.')
            if len(password1) < 3:
                raise forms.ValidationError('Пароль слишком короткий. Минимум 3 символа')
        return cleaned_data
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
    
class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control w-100', 'placeholder': 'Имя'}),
        }
        labels = {
            'name': 'Имя'
        }

class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Task.objects.all(),
        required=False,
        label="Статус",
        empty_label="---------"
    )
    assignee = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Исполнитель",
        empty_label="---------"
    )
    only_my_tasks = forms.BooleanField(required=False, label="Только свои задачи")