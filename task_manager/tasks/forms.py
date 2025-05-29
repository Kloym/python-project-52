from django import forms
from django.contrib.auth.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.core.cache import cache


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users_queryset = cache.get('all_users_queryset')
        if users_queryset is None:
            users_queryset = User.objects.only('id', 'username')
            cache.set('all_users_queryset', users_queryset, 3600)

        self.fields['assignee'].queryset = users_queryset

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
