from django.urls import path

from .views import GetGroupsListAPIView, GetGroupInfoAPIView


urlpatterns = [
    path("", GetGroupsListAPIView.as_view()),
    path("info/<group_number>", GetGroupInfoAPIView.as_view()),
]
