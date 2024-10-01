from django.shortcuts import render, redirect
from .models import Users
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import AddUserForm


def main_view(request):
    return render(request, 'main.html')

# Логика добавления нового пользователя
def add_user_view(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Проверяем, существует ли пользователь
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь с таким логином уже существует.')
            else:
                # Создаем нового пользователя
                User.objects.create_user(username=username, password=password)
                messages.success(request, 'Пользователь успешно добавлен.')
                return redirect('login')  # Перенаправляем обратно на страницу входа

    return render(request, 'add_user.html', {'form': AddUserForm()})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Проверяем, является ли пользователь администратором
            if request.POST.get('is_admin') and not user.is_staff:
                messages.error(request, "Access denied: Not an admin")
                return redirect('login')

            # Выполняем вход пользователя
            login(request, user)
            messages.success(request, f"Welcome {user.username}")
            return redirect('main_page')  # Перенаправление на главную страницу
        else:
            messages.error(request, "Неверный логин или пароль")

    return render(request, 'login.html')