from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Вы разлогинены")
    return redirect('index')

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
                return redirect('index')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        if 'next' in request.GET:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')

    return render(request, 'login.html', {'form': form})




