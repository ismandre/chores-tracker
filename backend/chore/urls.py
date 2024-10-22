from django.urls import path, include

from . import views

urlpatterns = [
    path('chores/create/', views.create_chore),
    path('chores/completed/', views.complete_chore),
    path('chores-by-urgency/', views.UrgentChoreList.as_view()),
    path('chores/<slug:room_slug>/<slug:chore_slug>', views.ChoreDetail.as_view()),
    path('chores/<slug:room_slug>/', views.RoomDetail.as_view()),
    path('rooms/', views.rooms),
]
