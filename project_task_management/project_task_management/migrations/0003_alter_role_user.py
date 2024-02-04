# Generated by Django 5.0.1 on 2024-02-03 09:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_task_management', '0002_rename_roles_role_rename_tasks_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='project_task_management.user'),
        ),
    ]
