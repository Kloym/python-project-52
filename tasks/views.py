from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskFilterForm

@login_required
def task_list(request):
    tasks = Task.objects.all()
    if request.method == 'GET':
        form = TaskFilterForm(request.GET)
        if form.is_valid():
            status = form.cleaned_data.get('status')
            assignee = form.cleaned_data.get('assignee')
            only_my_tasks = form.cleaned_data.get('only_my_tasks')
            if status:
                tasks = tasks.filter(status=status)
            if assignee:
                tasks = tasks.filter(assignee=assignee)
            if only_my_tasks:
                tasks = tasks.filter(author=request.user)
    else:
        form = TaskFilterForm()
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'form': form})
# Create your views here.
