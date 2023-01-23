from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from logs import models, serializers
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class CreateActivityView(generics.CreateAPIView):
    serializer_class = serializers.CreateActivitySerializer

class ListMoodLogView(generics.ListAPIView):
    serializer_class = serializers.ListMoodLogSerializer
    queryset = models.MoodLog.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'datetime': ['lt', 'gt', 'gte', 'lte', 'exact']}


class AddActivityView(generics.CreateAPIView):
    serializer_class = serializers.AddActivitySerializer

class CreateMoodLogView(generics.CreateAPIView):
    serializer_class = serializers.CreateMoodLogSerializer
