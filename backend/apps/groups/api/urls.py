from django.urls import path

from .views import GetGroupsListAPIView


urlpatterns = [
    path("", GetGroupsListAPIView.as_view()),
]
