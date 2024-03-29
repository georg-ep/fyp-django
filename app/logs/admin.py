from django.contrib import admin
from logs import models

# Register your models here.


@admin.register(models.MoodLog)
class MoodLog(admin.ModelAdmin):
  list_display = ("user", "created_at",)
  
@admin.register(models.BreathingExercise)
class BreathingExerciseAdmin(admin.ModelAdmin):
  list_display = ("name",)


@admin.register(models.BreathingCycle)
class BreathingCycleAdmin(admin.ModelAdmin):
  list_display = ("breathing_exercise", "created_at",)
  