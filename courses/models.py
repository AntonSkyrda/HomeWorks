from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Course(models.Model):
    name = models.CharField(_("Course Name"), max_length=255, unique=True)
    description = models.TextField(_("Course Description"))
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ManyToManyField(User, related_name="students", blank=True)

    def __str__(self):
        return self.name
