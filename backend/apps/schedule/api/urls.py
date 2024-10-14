from django.urls import path

from .views import (
    UpdateScheduleAPIView,
    GetAllScheduleAPIView,
    GetGroupScheduleAPIView,
    GetGlobalInfoAPIView,
)


urlpatterns = [
    path("update/", UpdateScheduleAPIView.as_view()),
    path("all/", GetAllScheduleAPIView.as_view()),
    path("info/", GetGlobalInfoAPIView.as_view()),
    path("<group_number>/", GetGroupScheduleAPIView.as_view()),
]
