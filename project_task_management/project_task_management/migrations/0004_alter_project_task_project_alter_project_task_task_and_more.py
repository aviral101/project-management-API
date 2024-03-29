# Generated by Django 5.0.1 on 2024-02-03 10:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_task_management', '0003_alter_role_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_task',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project', to='project_task_management.project'),
        ),
        migrations.AlterField(
            model_name='project_task',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task', to='project_task_management.task'),
        ),
        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='project_task_management.user'),
        ),
    ]
