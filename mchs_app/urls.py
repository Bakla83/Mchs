from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views  # Импортируем views здесь
from .views import admin_page, create_report, generate_task_report, generate_employee_report, \
    generate_department_report, generate_inspection_object_report, generate_inspection_report, departments, activity

urlpatterns = [
    path('', views.login_view, name='login'),  # Ссылаемся на views.login_view
    path('main/', views.MainView.as_view(), name='main_page'),  # Ссылаемся на views.main_view
    path('add_user/', views.add_user_view, name='add_user'),  # URL для добавления пользователя
    path('contacts/', TemplateView.as_view(template_name='contacts.html'), name='contacts'),
    path('admin/', admin_page, name='admin_page'),
    path('departments/', departments, name='departments'), # Отделения
    path('activity/', activity, name='activity'), # Деятельность
    path('create_report/', create_report, name='create_report'),  # Обработчик для создания отчета
    path('submit-tasks/', views.submit_tasks, name='submit_tasks'),  # Убедитесь, что это существует
    #path('create_report/', views.create_report, name='create_report'),
    path('all_reports/', views.all_reports, name='all_reports'),  # Все отчеты

    path('download_task_report/', generate_task_report, name='download_task_report'),
    path('download_employee_report/', generate_employee_report, name='download_employee_report'),
    path('download_department_report/', generate_department_report, name='download_department_report'),
    path('download_inspection_object_report/', generate_inspection_object_report,
         name='download_inspection_object_report'),
    path('download_inspection_report/', generate_inspection_report, name='download_inspection_report'),

]
