from django.contrib import admin

from .models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )


admin.site.register(Course, CourseAdmin)
