from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView


# Create your views here.
class IndexView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = False
        return context
    
    def form_valid(self, form):
        messages.success(self.request, _("Пользователь успешно зарегистрирован"))
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/update_user.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != request.user:
            messages.error(request, _('''У вас нет прав на изменение другого пользователя.'''))
            return redirect('user_list')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, _('Пользователь успешно изменен'))
        return super().form_valid(form)


class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
    context_object_name = 'user'

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if user != request.user:
            messages.error(request, _('''У вас нет прав на изменение другого пользователя.'''))
            return redirect('user_list')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = self.get_object()
        if user.tasks_created.exists():
            messages.error(self.request, _('''Нельзя удалить пользователя так как он используется'''))
            return redirect(self.success_url)
        messages.success(self.request, _('Пользователь успешно удален'))
        return super().form_valid(form)
