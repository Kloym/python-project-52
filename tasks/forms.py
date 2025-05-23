from django import forms
from django.contrib.auth.models import User
from .models import Status, Task
from labels.models import Label


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label="Статус",
        empty_label="---------",
    )
    assignee = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Исполнитель",
        empty_label="---------",
    )
    labels = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label="Метка",
        empty_label="---------",
    )
    only_my_tasks = forms.BooleanField(required=False, label="Только свои задачи")


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "assignee", "labels"]
        labels = {
            "name": "Имя",
            "description": "Описание",
            "status": "Статус",
            "assignee": "Исполнитель",
            "labels": "Метки",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Имя"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Описание"}),
            "labels": forms.CheckboxSelectMultiple(),
        }
