from rest_framework import generics
from logs import models, serializers
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.functions import TruncDate

# Create your views here.


class CreateActivityView(generics.CreateAPIView):
    serializer_class = serializers.CreateActivitySerializer

class ListMoodLogView(generics.ListAPIView):
    serializer_class = serializers.ListMoodLogSerializer
    queryset = models.MoodLog.objects.all()
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = {'datetime': ['lt', 'gt', 'gte', 'lte', 'exact']}

class ActivityListView(generics.ListAPIView):
    serializer_class =  serializers.ListActivityLogSerializer
    queryset = models.ActivityLog.objects.all()

class AddActivityView(generics.CreateAPIView):
    serializer_class = serializers.AddActivitySerializer

class CreateMoodLogView(generics.CreateAPIView):
    serializer_class = serializers.CreateMoodLogSerializer

class BreathingExerciseListView(generics.ListAPIView):
    serializer_class = serializers.ListBreathingExerciseSerializer
    queryset = models.BreathingExercise.objects.all()

class BreathingExerciseView(generics.RetrieveAPIView):
    serializer_class = serializers.ListBreathingExerciseSerializer
    queryset = models.BreathingExercise.objects.all()

class CreateBreathingCycleView(generics.CreateAPIView):
    serializer_class = serializers.CreateBreathingCycleSerializer
    queryset = models.BreathingCycle.objects.all()

class ListBreathingCycleView(generics.ListAPIView):
    serializer_class = serializers.ListBreathingCycleSerializer
    queryset = models.BreathingCycle.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'created_at': ['lt', 'gt', 'gte', 'lte', 'exact']}
    ordering_fields = ['created_at']


    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(date=TruncDate('created_at'))
        return qs

    def get_object(self):
        return self.request.user
