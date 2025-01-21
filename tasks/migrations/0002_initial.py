# Generated by Django 5.1.4 on 2025-01-21 11:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tasks", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="taskanswer",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="taskanswer",
            name="task",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="tasks.task"
            ),
        ),
        migrations.AddField(
            model_name="taskmark",
            name="task_answer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="tasks.taskanswer"
            ),
        ),
        migrations.AddField(
            model_name="taskmark",
            name="teacher",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]