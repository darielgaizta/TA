from rest_framework import serializers
from . import schedule

class PresetSerializer(serializers.Serializer):
    length = serializers.IntegerField()
    schedule = schedule.ScheduleSerializer(many=True)