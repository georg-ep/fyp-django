from rest_framework import generics
from logs import models, serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models.functions import TruncDate
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

class ListMoodLogView(generics.ListAPIView):
    serializer_class = serializers.ListMoodLogSerializer
    queryset = models.MoodLog.objects.all()
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = {'datetime': ['lt', 'gt', 'gte', 'lte', 'exact']}

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

class ListBreathingCycleView(APIView):
    
    def get(self, request, *args, **kwargs):
        ordering = request.GET.get("ordering", "-created_at")
        gte = request.GET.get("gte", None)
        lte = request.GET.get("lte", None)

        def get_datetime(date):
            return datetime.strptime(date, "%Y-%m-%d")

        cycles = models.BreathingCycle.objects.filter(mood_before__user=request.user).annotate(date=TruncDate('created_at')).order_by(ordering)
        
        if gte:
            cycles = cycles.filter(created_at__gte=get_datetime(gte))
        if lte:
            cycles = cycles.filter(created_at__lte=get_datetime(lte))
            

        def key_format(cycle):
            return f"{str(cycle[0].day).zfill(2)}-{str(cycle[0].month).zfill(2)}"
        
        dates = {key_format(cycle): [] for cycle in cycles.values_list("created_at").distinct()}

        for k in dates:
            day, month = k.split("-")[0], k.split("-")[1]
            filtered = cycles.filter(created_at__day=day, created_at__month=month).order_by("created_at")
            serializer = serializers.ListBreathingCycleSerializer(filtered, many=True)
            dates[k] = serializer.data
        
        return Response(dates)
