from django.db import models

class BreathingCycle(models.Model):
    breathing_exercise = models.ForeignKey("logs.BreathingExercise", on_delete=models.CASCADE)
    mood_before = models.ForeignKey("logs.MoodLog", on_delete=models.CASCADE, related_name="mood_before")
    mood_after = models.ForeignKey("logs.MoodLog", on_delete=models.CASCADE, related_name="mood_after")
    duration = models.TimeField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
       return " ".join([self.mood_before.user.email, self.breathing_exercise.name])

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
       return " ".join([self.user.email, str(self.created_at)])