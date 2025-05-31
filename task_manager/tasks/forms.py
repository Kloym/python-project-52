from django import forms
from django.contrib.auth.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

class UserProxy(User):
    class Meta:
        proxy = True

    def __str__(self):
        return self.get_full_name()

class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label="Статус",
        empty_label="---------",
    )
    executor = forms.ModelChoiceField(
        queryset=UserProxy.objects.all(),
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
    executor = forms.ModelChoiceField(
        queryset=UserProxy.objects.all(),
        label="Исполнитель"
    )
    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        labels = {
            "name": "Имя",
            "description": "Описание",
            "status": "Статус",
            "executor": "Исполнитель",
            "labels": "Метки",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Имя", "id": "id_name"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Описание", "id": "id_description"}),
            "status": forms.Select(attrs={"id": "id_status"}),
            "executor": forms.Select(attrs={"id": "id_executor"}),
            "labels": forms.SelectMultiple(attrs={"id": "id_labels"}),
        }