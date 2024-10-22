from django.urls import path

from . import views

urlpatterns = [
    path('assignees', views.AssigneeList.as_view())
]