from rest_framework import serializers
from logs import models
from rest_framework.serializers import ValidationError
from django.db.models import Q
from datetime import datetime


class ActivityColourSerializer(serializers.ModelSerializer):
    class Meta:
      model = models.ActivityColour
      fields = ("colour",)

class ActivitySerializer(serializers.ModelSerializer):
    colour = serializers.SerializerMethodField()

    class Meta:
      model = models.Activity
      fields = ("id", "name", "colour",)
    
    def get_colour(self, obj):
        colour = models.ActivityColour.objects.filter(activity=obj, user=self.context['request'].user)
        return "" if not colour else colour.first().colour


class AddActivitySerializer(serializers.ModelSerializer):

    class Meta:
      model = models.ActivityLog
      fields = ("start_time", "end_time", "activity", "user",)

class CreateActivitySerializer(serializers.ModelSerializer):
    colour = serializers.CharField(write_only=True)

    def create(self, validated_data):
      name = validated_data.get("name")
      user = self.context['request'].user
      colour = validated_data.get("colour")

      activity = models.Activity.objects.filter(name=name).first()

      if activity is None:
        activity = models.Activity.objects.create(name=name)
      
      activity_colour = models.ActivityColour.objects.filter(activity=activity, user=user).first()

      if activity_colour is None:
        activity_colour = models.ActivityColour.objects.create(activity=activity, user=user, colour=colour)
      else:
        activity_colour.colour = colour
        activity_colour.save()
        return activity

      if user in activity.users.all():
        raise ValidationError("User already has this activity")

      activity.users.add(user)

      return activity

    class Meta:
      model = models.Activity
      fields = ("name", "colour",)

class ListMoodLogSerializer(serializers.ModelSerializer):
    log_time = serializers.SerializerMethodField()

    class Meta:
      model = models.MoodLog
      fields = ("log_time", "notes", "level",)
    
    def get_log_time(self, obj):
      return obj.datetime.strftime("%H:%M")


class CreateMoodLogSerializer(serializers.ModelSerializer):

    def create(self, validated_data):

      log = models.MoodLog(**validated_data)
      
      if log.datetime is None:
        log.datetime = datetime.now()
      
      log.save()
      
      return log

    class Meta:
      model = models.MoodLog
      fields = ("user", "datetime", "notes", "level",)

          