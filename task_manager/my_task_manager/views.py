from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, "index.html")


def logout_view(request):
    logout(request)
    messages.info(request, "Вы разлогинены")
    return redirect("index")


class CustomLoginView(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy("user_list")
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Неверное имя пользователя или пароль")
        return super().form_invalid(form)
