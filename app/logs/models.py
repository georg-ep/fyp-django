from django.db import models
from datetime import datetime


class ActivityColour(models.Model):
    activity = models.ForeignKey("logs.Activity", on_delete=models.CASCADE, related_name="colour")
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    colour = models.CharField(max_length=255)

class Activity(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
      return self.name


class ActivityLog(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE,)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE,)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class MoodLog(models.Model):
    level = models.SmallIntegerField()
    notes = models.TextField(default="", null=True, blank=True)
    datetime = models.DateTimeField(null=True)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)

    class Meta:
      ordering = ["datetime"]