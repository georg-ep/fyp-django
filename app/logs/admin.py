from django.contrib import admin
from logs import models

# Register your models here.


@admin.register(models.MoodLog)
class MoodLog(admin.ModelAdmin):
  list_display = ("user",)
  

@admin.register(models.ActivityLog)
class ActivityLog(admin.ModelAdmin):
  # list_display = ("",)
  pass

@admin.register(models.Activity)
class Activity(admin.ModelAdmin):
  # list_display = ("",)
  pass

@admin.register(models.ActivityColour)
class ActivityColour(admin.ModelAdmin):
  # list_display = ("",)
  pass