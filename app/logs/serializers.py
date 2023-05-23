from rest_framework import serializers
from logs import models
from rest_framework.serializers import ValidationError
from django.db.models import Q
from datetime import datetime



class CreateBreathingCycleSerializer(serializers.ModelSerializer):
    mood_before = serializers.DictField(write_only=True)
    mood_after = serializers.DictField(write_only=True)

    def create(self, validated_data):
      mood_before = validated_data.get("mood_before")
      mood_after = validated_data.get("mood_after")
      mood_before["user_id"] = self.context["request"].user.id
      mood_after["user_id"] = self.context["request"].user.id

      objs = models.MoodLog.objects.bulk_create([models.MoodLog(**mood_before), models.MoodLog(**mood_after)])

      validated_data["mood_before"], validated_data["mood_after"] = objs[0], objs[1]
      
      return super().create(validated_data)

    class Meta:
        model = models.BreathingCycle
        fields = "__all__"


class ListMoodLogSerializer(serializers.ModelSerializer):
    class Meta:
      model = models.MoodLog
      fields = "__all__"

class ListBreathingExerciseSerializer(serializers.ModelSerializer):
    class Meta:
       model = models.BreathingExercise
       fields = "__all__"

class CreateMoodLogSerializer(serializers.ModelSerializer):
    class Meta:
      model = models.MoodLog
      fields = "__all__"

class ListBreathingCycleSerializer(serializers.ModelSerializer):
   date = serializers.SerializerMethodField()
   mood_before = ListMoodLogSerializer()
   mood_after = ListMoodLogSerializer()
  #  breathing_exercise = ListBreathingExerciseSerializer()
   duration = serializers.SerializerMethodField()
   time = serializers.SerializerMethodField()
   exercise = serializers.SerializerMethodField()

   class Meta:
      model = models.BreathingCycle
      fields = "__all__"
  
   def get_exercise(self, obj):
      return obj.breathing_exercise.name

   def get_date(self, obj):
      return obj.date
   
   def get_time(self, obj):
      return obj.created_at.strftime("%H:%M")
  
   def get_duration(self, obj):
      mins = obj.duration.strftime("%M").strip("0")
      sec = obj.duration.strftime("%S").strip("0")
      return f"{mins}m {sec}s" if mins else f"{sec}s"