from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Task
from .forms import TaskFilterForm
from .forms import TaskCreateForm

@login_required
def task_list(request):
    tasks = Task.objects.all()
    if request.method == 'GET':
        form = TaskFilterForm(request.GET)
        if form.is_valid():
            only_my_tasks = form.cleaned_data.get('only_my_tasks')
            status = form.cleaned_data.get('status')
            assignee = form.cleaned_data.get('assignee')
            labels = form.cleaned_data.get('labels')
            if status:
                tasks = tasks.filter(status=status)
            if assignee:
                tasks = tasks.filter(assignee=assignee)
            if labels:
                tasks = tasks.filter(labels=labels)
            if only_my_tasks:
                tasks = tasks.filter(author=request.user)
    context = {
        'tasks': tasks,
        'form': form,
    }
    return render(request, 'tasks/task_list.html', context)

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            form.save_m2m()
            messages.success(request, 'Задача успешно создана')
            return redirect('task_list')
        else:
            messages.error(request, 'Ошибка при создании задачи. Пожалуйста, проверьте данные.')
    else:
        form = TaskCreateForm()
    return render(request, 'tasks/create_task.html', {'form': form})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.author != request.user:
        messages.error(request, 'Задачу может удалить только ее автор')
        return redirect('task_list')
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Задача успешно удалена')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskCreateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача успешно изменена')
            return redirect('task_list')
    else:
        form = TaskCreateForm(instance=task)
    return render(request, 'tasks/task_update.html', {'form': form})

def get(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_view.html', {'task': task})
    
