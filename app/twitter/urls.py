from django.urls import path
from twitter import views

urlpatterns = [
  path("tweets/<str:username>/", views.TweetListApiView.as_view(), name="")
]