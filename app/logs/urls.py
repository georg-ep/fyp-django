from django.urls import path
from logs import views

urlpatterns = [
  path("mood/create/", views.CreateMoodLogView.as_view(), name="create-mood"),
  path("mood/list/", views.ListMoodLogView.as_view(), name="list-mood"),
  path("activity/create/", views.CreateActivityView.as_view(), name="create-activity"),
  path("activity/add/", views.AddActivityView.as_view(), name="add-activity"),
]