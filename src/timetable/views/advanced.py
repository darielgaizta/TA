"""
Author: Dariel Gaizta

Advanced view is used to handle more complex request. The request will take a preset schedule based
on lecturers' preference. In this case, serializers.PresetSerializer will be used. Lecturers are able
to do the following:
1. Assigned his/her Course to a specific Room and/or Timeslot.
2. Teach one or more courses, the timeslot gap will be adjusted.

Future Development: advanced.py will be deleted and migrated to preset.py
"""

from django.db.models import Prefetch
from .. import models, serializers

def advanced(request):
    if request.method == 'POST':
        serializer = serializers.PresetSerializer(data=request.data, many=True)
        if serializer.is_valid():
            timetable = {}
            timeslots = models.Timeslot.objects.all()
            locations = models.Location.objects.prefetch_related(
                Prefetch('room_set', queryset=models.Room.objects.order_by('id')))
            
            for data in serializer.validated_data:
                pass