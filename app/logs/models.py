from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime


class SimpleActivity(models.Model):
    name = models.CharField(max_length=255)

class CustomUserActivity(models.Model):
    name = models.CharField(max_length=255)
    has_value = models.BooleanField(default=False)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="custom_activities")

    class Meta:
      verbose_name_plural = "Custom Activities"

class Activity(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
      return self.name

    class Meta:
      verbose_name_plural = "Activities"


class ActivityLog(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE,)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)
    custom_activity = models.ForeignKey(CustomUserActivity, on_delete=models.CASCADE, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(default="", null=True, blank=True)
    mood_level = models.PositiveIntegerField()

    # Validate at least one type of actiivty included
    def clean(self):
        if not self.activity or self.custom_activity:
          raise ValidationError("One type of activity must be included")

class BreathingCycle(models.Model):
    breathing_exercise = models.ForeignKey("logs.BreathingExercise", on_delete=models.CASCADE)
    mood_before = models.ForeignKey("logs.MoodLog", on_delete=models.CASCADE, related_name="mood_before")
    mood_after = models.ForeignKey("logs.MoodLog", on_delete=models.CASCADE, related_name="mood_after")
    duration = models.TimeField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
       return " ".join([self.mood_before.user.username, self.breathing_exercise.name])

class BreathingExercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="", null=True, blank=True)
    reference = models.URLField(default=None, null=True, blank=True)
    overview = models.TextField(default="", null=True, blank=True)
    inhale = models.SmallIntegerField()
    inhale_notes = models.TextField(default="", null=True, blank=True)
    hold_inhale = models.SmallIntegerField()
    hold_inhale_notes = models.TextField(default="", null=True, blank=True)
    exhale = models.SmallIntegerField()
    exhale_notes = models.TextField(default="", null=True, blank=True)
    hold_exhale = models.SmallIntegerField()
    hold_exhale_notes = models.TextField(default="", null=True, blank=True)

    def __str__(self):
        return self.name

class MoodLog(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    stress = models.SmallIntegerField(default=0)
    focus = models.SmallIntegerField(default=0)
    anger = models.SmallIntegerField(default=0)
    notes = models.TextField(default="", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
      ordering = ["created_at"]

    def __str__(self):
       return " ".join([self.user.username, str(self.created_at)])