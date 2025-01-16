from django.db import models
from django.utils.translation import gettext_lazy as _

from courses.models import Course


class Lesson(models.Model):
    title = models.CharField(_("Lesson Title"), max_length=255)
    description = models.TextField(_("Lesson Description"))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")

    def __str__(self):
        return self.title
