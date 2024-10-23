from django.shortcuts import render, redirect, get_object_or_404
from .models import Users, Employee, Task, Report, Inspection, Violation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import ListView
from .forms import AddUserForm, EmployeeForm, TaskForm
from .models import Task
from django.db import models
from django.http import HttpResponse
from docxtpl import DocxTemplate
import os

def all_reports(request):
    reports = Report.objects.all()
    return render(request, 'all_reports.html', {'reports': reports})

class MainView(ListView):
    template_name = "main.html"
    model = Task

#def main_view(request):
#
#    return render(request, 'main.html')

# Отделения
def departments(request):
   return render(request, 'departments.html')

# Деятельность
def activity(request):
   return render(request, 'activity.html')

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

# Логика входа
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

# Страница администрирования
def admin_page(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == 'baklan':
            return render(request, 'admin_dashboard.html')  # Отображение страницы администрирования
        else:
            messages.error(request, 'Неверный пароль. Попробуйте снова.')
    return render(request, 'admin_login.html')  # Страница ввода пароля

# Создание отчета
def create_report(request):
    if request.method == 'POST':
        report_name = request.POST.get('report_name')
        employee_name = request.POST.get('employee_name')
        report_date = request.POST.get('report_date')
        department = request.POST.get('department')
        address = request.POST.get('address')

        report = Report(
            report_name=report_name,
            employee_name=employee_name,
            report_date=report_date,
            department=department,
            address=address,
        )
        report.save()
        return redirect('admin_page')  # Перенаправление после успешного создания отчета
    return redirect('admin_page')  # В случае другого метода

# Задания
def submit_tasks(request):
    if request.method == 'POST':
        return render(request, 'submit_tasks.html')
    return render(request, 'submit_tasks.html')

# Управление работниками
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = EmployeeForm()
    return render(request, 'admin/add_employee.html', {'form': form})

def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'admin/edit_employee.html', {'form': form})

def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    employee.delete()
    return redirect('admin_page')

# Добавить сотрудника
def add_employee(request):
    if request.method == 'POST':
        employee_name = request.POST.get('employee_name')
        department = request.POST.get('department')

        employee = Employee(employee_name=employee_name, department=department)
        employee.save()
        messages.success(request, 'Сотрудник успешно добавлен')
        return redirect('admin_dashboard')
    return render(request, 'add_employee.html')

# Удалить сотрудника
def delete_employee(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        employee.delete()
        messages.success(request, 'Сотрудник успешно удалён')
    except Employee.DoesNotExist:
        messages.error(request, 'Сотрудник не найден')
    return redirect('admin_dashboard')

# Добавить задание
def add_task(request):
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        description = request.POST.get('description')
        status = request.POST.get('status')
        date = request.POST.get('date')

        task = Task(task_name=task_name, description=description, status=status, date=date)
        task.save()
        messages.success(request, 'Задание успешно добавлено')
        return redirect('admin_dashboard')
    return render(request, 'add_task.html')

# Редактировать задание
def edit_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        if request.method == 'POST':
            task.task_name = request.POST.get('task_name')
            task.description = request.POST.get('description')
            task.status = request.POST.get('status')
            task.date = request.POST.get('date')
            task.save()
            messages.success(request, 'Задание успешно обновлено')
            return redirect('admin_dashboard')
        return render(request, 'edit_task.html', {'task': task})
    except Task.DoesNotExist:
        messages.error(request, 'Задание не найдено')
        return redirect('admin_dashboard')


def create_report(request):
    if request.method == 'POST':
        inspection_id = request.POST.get('inspection_id')  # ID существующей инспекции
        report_date = request.POST.get('report_date')

        # Получаем выбранную инспекцию
        try:
            inspection = Inspection.objects.get(pk=inspection_id)
        except Inspection.DoesNotExist:
            messages.error(request, 'Инспекция не найдена.')
            return redirect('create_report')

        # Создаём новый отчёт
        report = Report(report_date=report_date, inspection=inspection)
        report.save()

        messages.success(request, 'Отчёт успешно создан.')
        return redirect('admin_page')

        # Если GET-запрос, отображаем форму с инспекциями
    inspections = Inspection.objects.all()
    return render(request, 'create_report.html', {'inspections': inspections})





import os
from django.http import HttpResponse
from django.utils import timezone
from django.db import connection
from docxtpl import DocxTemplate


# Базовый путь для сохранения отчетов
BASE_REPORT_PATH = "C:/Users/263/PycharmProjects/МЧС_РПБД/mchs_app/отчеты/"

def generate_task_report(request):
    # Выполнение SQL-запроса для получения данных о задачах через подключение Django
    tasks = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, title, description, status, due_date FROM dbo.mchs_app_task")
        rows = cursor.fetchall()

        for row in rows:
            tasks.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'status': row[3],
                'due_date': row[4],
            })

    # Путь к шаблону
    template_path = "C:\\Users\\263\\PycharmProjects\\МЧС_РПБД\\mchs_app\\отчеты\\task_report_template.docx"
    report_path = "C:\\Users\\263\\PycharmProjects\\МЧС_РПБД\\mchs_app\\отчеты\\отчет_задач.docx"

    # Загрузка шаблона
    doc = DocxTemplate(template_path)

    # Контекст для заполнения шаблона
    context = {
        'tasks': tasks,
        'current_date': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),  # Текущая дата
    }

    # Заполнение шаблона
    doc.render(context)

    # Сохранение сгенерированного отчета
    doc.save(report_path)

    # Возврат файла в качестве ответа
    with open(report_path, 'rb') as report_file:
        response = HttpResponse(report_file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(report_path)}'
        return response



def generate_employee_report(request):
    # Выполнение SQL-запроса для получения данных о сотрудниках через подключение Django
    employees = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT employee_id, name, position, department_id FROM dbo.mchs_app_employee")
        rows = cursor.fetchall()

        for row in rows:
            employees.append({
                'employee_id': row[0],
                'name': row[1],
                'position': row[2],
                'department_id': row[3],
            })

    # Путь к шаблону
    template_path = "C:\\Users\\263\\PycharmProjects\\МЧС_РПБД\\mchs_app\\отчеты\\employee_report_template.docx"
    report_path = "C:\\Users\\263\\PycharmProjects\\МЧС_РПБД\\mchs_app\\отчеты\\отчет_сотрудников.docx"

    # Загрузка шаблона
    doc = DocxTemplate(template_path)

    # Контекст для заполнения шаблона
    context = {
        'employees': employees,
        'current_date': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),  # Текущая дата
    }

    # Заполнение шаблона
    doc.render(context)

    # Сохранение сгенерированного отчета
    doc.save(report_path)

    # Возврат файла в качестве ответа
    with open(report_path, 'rb') as report_file:
        response = HttpResponse(report_file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(report_path)}'
        return response


def generate_department_report(request):
    # Выполнение SQL-запроса для получения данных об отделах через подключение Django
    departments = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT department_id, department_name, address FROM dbo.mchs_app_department")
        rows = cursor.fetchall()

        for row in rows:
            departments.append({
                'department_id': row[0],
                'department_name': row[1],
                'address': row[2],
            })

    # Путь к шаблону
    template_path = "C:\\Users\\263\\PycharmProjects\\МЧС_РПБД\\mchs_app\\отчеты\\department_report_template.docx"
    report_path = "C:\\Users\\263\\PycharmProjects\\МЧС_РПБД\\mchs_app\\отчеты\\отчет_отделов.docx"

    # Загрузка шаблона
    doc = DocxTemplate(template_path)

    # Контекст для заполнения шаблона
    context = {
        'departments': departments,
        'current_date': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),  # Текущая дата
    }

    # Заполнение шаблона
    doc.render(context)

    # Сохранение сгенерированного отчета
    doc.save(report_path)

    # Возврат файла в качестве ответа
    with open(report_path, 'rb') as report_file:
        response = HttpResponse(report_file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(report_path)}'
        return response

def generate_inspection_object_report(request):
        # Выполнение SQL-запроса для получения данных об объектах инспекции через подключение Django
        inspection_objects = []
        with connection.cursor() as cursor:
            cursor.execute("SELECT TOP (1000) object_id, object_name, address FROM dbo.InspectionObject")
            rows = cursor.fetchall()

            for row in rows:
                inspection_objects.append({
                    'object_id': row[0],
                    'object_name': row[1],
                    'address': row[2],
                })

        # Путь к шаблону
        template_path = "C:\\Users\\263\\PycharmProjects\\МЧС_РПБД\\mchs_app\\отчеты\\inspection_object_report_template.docx"
        report_path = "C:\\Users\\263\\PycharmProjects\\МЧС_РПБД\\mchs_app\\отчеты\\отчет_объектов_инспекции.docx"

        # Загрузка шаблона
        doc = DocxTemplate(template_path)

        # Контекст для заполнения шаблона
        context = {
            'inspection_objects': inspection_objects,
            'current_date': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),  # Текущая дата
        }

        # Заполнение шаблона
        doc.render(context)

        # Сохранение сгенерированного отчета
        doc.save(report_path)

        # Возврат файла в качестве ответа
        with open(report_path, 'rb') as report_file:
            response = HttpResponse(report_file.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(report_path)}'
            return response


def generate_inspection_report(request):
        # Выполнение SQL-запроса для получения данных об инспекциях через подключение Django
        inspections = []
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT TOP (1000) inspection_id, inspection_date, employee_id, object_id FROM dbo.mchs_app_inspection")
            rows = cursor.fetchall()

            for row in rows:
                inspections.append({
                    'inspection_id': row[0],
                    'inspection_date': row[1],
                    'employee_id': row[2],
                    'object_id': row[3],
                })

        # Путь к шаблону
        template_path = "C:\\Users\\263\\PycharmProjects\\МЧС_РПБД\\mchs_app\\отчеты\\inspection_report_template.docx"
        report_path = "C:\\Users\\263\\PycharmProjects\\МЧС_РПБД\\mchs_app\\отчеты\\отчет_инспекций.docx"

        # Загрузка шаблона
        doc = DocxTemplate(template_path)

        # Контекст для заполнения шаблона
        context = {
            'inspections': inspections,
            'current_date': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),  # Текущая дата
        }

        # Заполнение шаблона
        doc.render(context)

        # Сохранение сгенерированного отчета
        doc.save(report_path)

        # Возврат файла в качестве ответа
        with open(report_path, 'rb') as report_file:
            response = HttpResponse(report_file.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(report_path)}'
            return response