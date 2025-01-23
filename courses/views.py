from django.views.generic import ListView, DetailView

from .models import Course


class CourseListView(ListView):
    model = Course
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.prefetch_related(
            "student",
            "lessons",
            "task_set",
        ).select_related(
            "teacher",
        )


class CourseDetailView(DetailView):
    model = Course
