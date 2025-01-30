from django.urls import path

from .views import CourseListView, CourseDetailView, IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("courses/", CourseListView.as_view(), name="course_list"),
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
]

app_name = "courses"
