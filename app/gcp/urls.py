from django.urls import path
from gcp import views

urlpatterns = [
  path('auth/user/', views.GoogleAuthUser.as_view()),
  path('auth/user/facebook/', views.FacebookAuthUser.as_view())
]