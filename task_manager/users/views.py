from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm


# Create your views here.
def user_list(request):
    users = User.objects.all()
    return render(request, "users/user_list.html", {"users": users})


def user_create(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            messages.success(request, "Пользователь успешно зарегистрирован")
            return redirect("login")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = UserRegistrationForm()
    return render(request, "registration.html", {"form": form})


@login_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Пользователь успешно изменен")
            return redirect("user_list")
    else:
        form = UserRegistrationForm(instance=user)
    return render(request, "users/update_user.html", {"form": form})


@login_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        messages.success(request, "Пользователь успешно удален")
        return redirect("user_list")
    return render(request, "users/user_confirm_delete.html", {"user": user})
