from django.db import models

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True)

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=50)
    due_date = models.DateField()

    def __str__(self):
        return self.title


class InspectionObject(models.Model):
    object_id = models.AutoField(primary_key=True)
    object_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)

class Inspection(models.Model):
    inspection_id = models.AutoField(primary_key=True)
    inspection_date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    object = models.ForeignKey(InspectionObject, on_delete=models.CASCADE)

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    report_date = models.DateField()
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE)

class Violation(models.Model):
    violation_id = models.AutoField(primary_key=True)
    description = models.TextField()
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE)

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50)

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
