from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label


class IndexView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/label_list.html"
    context_object_name = "labels"


class LabelCreateView(LoginRequiredMixin, CreateView):
    form_class = LabelForm
    template_name = "labels/create_label.html"
    success_url = reverse_lazy("label_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = False
        return context

    def form_valid(self, form):
        messages.success(self.request, _("Метка успешно создана"))
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/label_update.html"
    success_url = reverse_lazy("label_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, _("Метка успешно изменена"))
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/label_confirm_delete.html"
    success_url = reverse_lazy("label_list")
    context_object_name = "label"

    def form_valid(self, form):
        label = self.get_object()
        if label.task_set.exists():
            messages.error(
                self.request, _("Невозможно удалить метку, потому что она используется")
            )
            return redirect(self.success_url)
        messages.success(self.request, _("Метка успешно удалена"))
        return super().form_valid(form)
