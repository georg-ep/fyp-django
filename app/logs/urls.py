from django.urls import path
from logs import views

urlpatterns = [
  path("mood/create/", views.CreateMoodLogView.as_view(), name="create-mood"),
  path("mood/list/", views.ListMoodLogView.as_view(), name="list-mood"),
  path("breathing_exercises/all/", views.BreathingExerciseListView.as_view(), name="breathing-exercises"),
  path("breathing_exercises/<int:pk>/", views.BreathingExerciseView.as_view(), name="breathing-exercise"),
  path("breathing_cycle/create/", views.CreateBreathingCycleView.as_view(), name="create-cycle"),
  path("breathing_cycle/list/", views.ListBreathingCycleView.as_view(), name="list-cycles"),
]