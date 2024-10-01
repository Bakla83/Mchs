from django.shortcuts import render, redirect
from .models import Users
from django.contrib.auth import authenticate, login
from django.contrib import messages


def main_view(request):
    return render(request, 'main.html')

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