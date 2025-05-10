from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .forms import UserForm, StatusForm
from .models import Status
import re

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login_index(request):
    return render(request, 'login_index.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Вы разлогинены")
    return redirect('index')

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def status_list(request):
    statuses = Status.objects.all()
    return render(request, 'status_list.html', {'statuses': statuses})

def user_create(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username_pattern = re.compile(r'^[\w.@+-]+$')
        if not username:
            messages.error(request, 'Имя пользователя обязательно')
        elif len(username) > 150:
            messages.error(request, 'Имя пользователя не должно превышать 150 символов')
        elif not username_pattern.match(username):
            messages.error(request, 'Имя пользователя содержит недопустимые символы')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
        
        if not password1:
            messages.error(request, 'Пароль обязателен')
        elif len(password1) < 3:
            messages.error(request, 'Ваш пароль должен содержать как минимум 3 символа')
        elif password1 != password2:
            messages.error(request, 'Пароли не совпадают')
        else:
            try:
                validate_password(password1)
            except ValidationError as e:
                for err in e.messages:
                    messages.error(request, err)
        if messages.get_messages(request):
            return render(request, 'registration.html', {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
            })
        
        # Создание пользователя
        user = User.objects.create_user(
            username=username,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        messages.success(request, 'Пользователь успешно зарегистрирован')
        return redirect('login')
    
    return render(request, 'registration.html')

def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы залогинены')
                return redirect('login_index')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')

    return render(request, 'login.html', {'form': form})


def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно изменен')
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'update_user.html', {'form': form})

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Пользователь успешно удален')
        return redirect('user_list')
    return render(request, 'user_confirm_delete.html', {'user': user})

def create_status(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('status_list')
    else:
        form = StatusForm()
    return render(request, 'create_status.html', {'form': form})




