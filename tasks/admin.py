from django.contrib import admin

from .models import Task, TaskAnswer, TaskMark


class TaskAdmin(admin.ModelAdmin):
    list_display = ("description",)


class TaskAnswerAdmin(admin.ModelAdmin):
    list_display = ("description",)


class TaskMarkAdmin(admin.ModelAdmin):
    list_display = ("date", "mark")


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskAnswer, TaskAnswerAdmin)
admin.site.register(TaskMark, TaskMarkAdmin)
