from django.contrib import admin
# мне нужно настроить администрирование, придумай что может делать администратор с имеющимися данными
# Register your models here.
from django.contrib import admin
from .models import Employee, Task, Department

admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(Department)