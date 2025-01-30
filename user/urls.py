from django.urls import path

from .views import (
    UserLogoutView,
    UserLoginView,
    RegisterView,
    UserDashboardView,
    CourseDetailView,
    TaskAnswerFormView,
)

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("dashboard/", UserDashboardView.as_view(), name="dashboard"),
    path("course/<int:course_id>/", CourseDetailView.as_view(), name="course_detail"),
    path(
        "task/submit/<int:course_id>/<int:task_id>/",
        TaskAnswerFormView.as_view(),
        name="submit_task_answer",
    ),
]

app_name = "user"
