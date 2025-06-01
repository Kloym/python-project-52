from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskFilterForm, UserProxy
from task_manager.tasks.forms import TaskCreateForm
from task_manager.labels.models import Label
from task_manager.statuses.models import Status


@login_required
def task_list(request):
    tasks = Task.objects.all().order_by('id')
    form = TaskFilterForm(request.GET or None)
    filters_applied = False
    if form.is_valid():
        filters = {}
        if form.cleaned_data.get("status"):
            filters['status'] = form.cleaned_data["status"]
        if form.cleaned_data.get("executor"):
            filters['executor'] = form.cleaned_data["executor"]
        if form.cleaned_data.get("labels"):
            filters['labels__in'] = form.cleaned_data["labels"]
        if form.cleaned_data.get("only_my_tasks"):
            filters['author'] = request.user

        if filters:
            tasks = tasks.filter(**filters)
            filters_applied = True
    context = {
        "tasks": tasks,
        "form": form,
        "filters_applied": filters_applied,
    }
    return render(request, "tasks/task_list.html", context)


@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.name = "first task name"
            try:
                task.status = Status.objects.get(name="Op")
            except Status.DoesNotExist:
                # Обработайте ситуацию, если статус "Op" не существует
                print("Ошибка: Статус 'Op' не найден в базе данных!")
                return render(request, "tasks/create_task.html", {"form": form, "error": "Статус 'Op' не найден"})
            try:
                task.executor = UserProxy.objects.first()
                if task.executor is None:
                    print("Ошибка: Нет исполнителей в UserProxy!")
                    return render(request, "tasks/create_task.html", {"form": form, "error": "Нет исполнителей"})
            except UserProxy.DoesNotExist:
                print("Ошибка: Не найден исполнитель!")
                return render(request, "tasks/create_task.html", {"form": form, "error": "Не найден исполнитель"})
            labels = []
            try:
                labels.append(Label.objects.get(name="Gh"))
                labels.append(Label.objects.get(name="Пр"))
                task.save()
                for label in labels:
                   task.labels.add(label)
                form.save_m2m()
            except Label.DoesNotExist:
                print("Ошибка: Одна или несколько меток не найдены!")
                return render(request, "tasks/create_task.html", {"form": form, "error": "Одна или несколько меток не найдены"})
            task.save()
            form.save_m2m()
            messages.success(request, "Задача успешно создана")
            return redirect("task_list")
    else:
        form = TaskCreateForm()

    return render(request, "tasks/create_task.html", {"form": form})


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.author != request.user:
        messages.error(request, "Задачу может удалить только ее автор")
        return redirect("task_list")
    if request.method == "POST":
        task.delete()
        messages.success(request, "Задача успешно удалена")
        return redirect("task_list")
    return render(request, "tasks/task_confirm_delete.html", {"task": task})


@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskCreateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Задача успешно изменена")
            return redirect("task_list")
    else:
        form = TaskCreateForm(instance=task)
    return render(request, "tasks/task_update.html", {"form": form})


def get(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "tasks/task_view.html", {"task": task})
