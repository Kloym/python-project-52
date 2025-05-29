from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskFilterForm
from task_manager.tasks.forms import TaskCreateForm


@login_required
def task_list(request):
    tasks = Task.objects.all().select_related('status', 'author', 'assignee').prefetch_related('labels')
    form = TaskFilterForm(request.GET or None)
    filters_applied = False
    if form.is_valid():
        filters = {}
        if form.cleaned_data.get("status"):
            filters['status'] = form.cleaned_data["status"]
        if form.cleaned_data.get("assignee"):
            filters['assignee'] = form.cleaned_data["assignee"]
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
            try:
                task = form.save(commit=False)
                task.author = request.user
                task.save()
                form.save_m2m()
                messages.success(request, "Задача успешно создана")
                return redirect("task_list")
            except Exception as e:
                messages.error(request, f"Ошибка при сохранении задачи: {e}")
                print(f"Ошибка при сохранении задачи: {e}")
        else:
            messages.error(
                request, "Ошибка при создании задачи. Пожалуйста, проверьте данные."
            )
            print("Ошибки формы:", form.errors)
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
