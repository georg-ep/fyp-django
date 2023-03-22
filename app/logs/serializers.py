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

class ListActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ActivityLog
        fields = ("start_time",)

class ActivitySerializer(serializers.ModelSerializer):
    is_custom = serializers.ReadOnlyField(default=False)
    class Meta:
      model = models.Activity
      fields = ("name", "id", "is_custom",)

class CustomActivitySerializer(serializers.ModelSerializer):
    is_custom = serializers.ReadOnlyField(default=True)
    class Meta:
      model = models.CustomUserActivity
      fields = ("name", "has_value", "id", "is_custom",)

class AddActivitySerializer(serializers.ModelSerializer):
    activity = serializers.IntegerField(write_only=True, required=True)
    # is_custom = serializers.BooleanField(read_only=True, required=True)

    # def create(self, validated_data):
    #    activity_id = validated_data.get("activity")
    #    is_custom = validated_data.get("is_custom")

    #    activity = models.CustomUserActivity.objects.get(id=activity) if is_custom else models.Activity.objects.get(id=activity)


    class Meta:
      model = models.ActivityLog
      fields = ("value", "activity", "user", "start_time", "end_time",)

class CreateActivitySerializer(serializers.ModelSerializer):
    def create(self, validated_data):
      
      name = validated_data.get("name")
      user =  self.context['request'].user

      if models.CustomUserActivity.objects.filter(user=user, name__iexact=name).exists():
        raise ValidationError("User has an activity with this name")
      
      return super().create(validated_data)

    class Meta:
      model = models.CustomUserActivity
      fields = ("name", "user", "has_value",)

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
   breathing_exercise = ListBreathingExerciseSerializer()
   duration = serializers.SerializerMethodField()
   time = serializers.SerializerMethodField()

   class Meta:
      model = models.BreathingCycle
      fields = "__all__"

   def get_date(self, obj):
      return obj.date
   
   def get_time(self, obj):
      return obj.created_at.strftime("%H:%M")
  
   def get_duration(self, obj):
      mins = obj.duration.strftime("%M").strip("0")
      sec = obj.duration.strftime("%S").strip("0")
      # print(self.context["request"].GET.get("created_at__lte"))
      # print(self.context["request"].GET.get("created_at__gte"))
      return f"{mins}m {sec}s" if mins else f"{sec}s"