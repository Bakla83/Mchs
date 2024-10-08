# Generated by Django 5.0.9 on 2024-09-25 10:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.AutoField(primary_key=True, serialize=False)),
                ('department_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InspectionObject',
            fields=[
                ('object_id', models.AutoField(primary_key=True, serialize=False)),
                ('object_name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_id', models.AutoField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=100)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mchs_app.department')),
            ],
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('inspection_id', models.AutoField(primary_key=True, serialize=False)),
                ('inspection_date', models.DateField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mchs_app.employee')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mchs_app.inspectionobject')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.AutoField(primary_key=True, serialize=False)),
                ('report_date', models.DateField()),
                ('inspection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mchs_app.inspection')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mchs_app.role')),
            ],
        ),
        migrations.CreateModel(
            name='Violation',
            fields=[
                ('violation_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('inspection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mchs_app.inspection')),
            ],
        ),
    ]
