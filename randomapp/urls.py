from django.urls import path

from .views import RandomStringView


urlpatterns = [
    path("random/", RandomStringView.as_view(), name="random"),
]
