from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views  # Импортируем views здесь

urlpatterns = [
    path('', views.login_view, name='login'),  # Ссылаемся на views.login_view
    path('main/', views.main_view, name='main_page'),  # Ссылаемся на views.main_view
    path('add_user/', views.add_user_view, name='add_user'),  # URL для добавления пользователя

    path('contacts/', TemplateView.as_view(template_name='contacts.html'), name='contacts'),


]
