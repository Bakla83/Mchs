from django.contrib import admin
from django.urls import path, include
from . import views  # Импортируем views здесь

urlpatterns = [
    path('', views.login_view, name='login'),  # Ссылаемся на views.login_view
    path('main/', views.main_view, name='main_page'),  # Ссылаемся на views.main_view
]
