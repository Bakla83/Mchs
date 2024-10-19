from django.test import TestCase
from django.urls import reverse
from .models import Report, Inspection, Task, Employee
from django.contrib.auth.models import User

class ReportTests(TestCase):
    def setUp(self):
        # Создаем данные для теста
        self.inspection = Inspection.objects.create(
            inspection_date='2024-10-10',
            employee_id=1,
            object_id=1
        )

    def test_create_report_valid_data(self):
        response = self.client.post(reverse('create_report'), {
            'inspection_id': self.inspection.id,
            'report_date': '2024-10-15'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Report.objects.filter(inspection=self.inspection).exists())

    def test_create_report_missing_title(self):
        response = self.client.post(reverse('create_report'), {
            'inspection_id': '',
            'report_date': '2024-10-15'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Название отчета обязательно для заполнения")

class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin123')

    def test_login_with_correct_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'admin123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main_page'))

    def test_login_with_wrong_password(self):
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Неверный логин или пароль")

class TaskTests(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            first_name='Иван',
            last_name='Иванов',
            position='Инспектор',
            department_id=1
        )

    def test_add_task_valid_data(self):
        response = self.client.post(reverse('add_task'), {
            'title': 'Проверка пожарной сигнализации',
            'description': 'Провести проверку оборудования.',
            'due_date': '2024-10-15',
            'employee_id': self.employee.id,
            'status': 'Ожидает выполнения'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='Проверка пожарной сигнализации').exists())
