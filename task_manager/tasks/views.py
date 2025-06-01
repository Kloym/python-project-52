from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskFilterForm
from task_manager.tasks.forms import TaskCreateForm
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


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


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('task_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = False
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, _("Задача успешно создана"))
        return super().form_valid(form)


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
