from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView


class IndexView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/index.html"
    context_object_name = "statuses"


class StatusCreateView(LoginRequiredMixin, CreateView):
    form_class = StatusForm
    template_name = "statuses/create_status.html"
    success_url = reverse_lazy("status_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = False
        return context

    def form_valid(self, form):
        messages.success(self.request, _("Статус успешно создан"))
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/status_update.html"
    success_url = reverse_lazy("status_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, _("Статус успешно изменен"))
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "statuses/status_confirm_delete.html"
    success_url = reverse_lazy("status_list")
    context_object_name = "status"

    def form_valid(self, form):
        status = self.get_object()
        if status.task_set.exists():
            messages.error(
                self.request, 
                _("Невозможно удалить статус так как он используется")
            )
            return redirect(self.success_url)
        messages.success(self.request, _("Статус успешно удален"))
        return super().form_valid(form)
