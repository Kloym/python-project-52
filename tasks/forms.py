from django import forms
from django.contrib.auth.models import User
from .models import Task

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