from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from courses.models import Course


User = get_user_model()


class Task(models.Model):
    description = models.TextField(_("Task description"))
    max_marks = models.PositiveIntegerField(_("Maximum mark"))
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class TaskAnswer(models.Model):
    description = models.TextField(_("Answer description"))
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    mark = models.PositiveIntegerField(_("Task mark"), blank=True, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class TaskMark(models.Model):
    date = models.DateField(_("Task date"))
    mark = models.PositiveIntegerField(_("Task mark"))
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    task_answer = models.ForeignKey("TaskAnswer", on_delete=models.CASCADE)
