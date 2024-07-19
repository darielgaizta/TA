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
from rest_framework.exceptions import ValidationError
from .. import models, serializers

def advanced(request):
    if request.method == 'POST':
        serializer = serializers.AdvancedSerializer(data=request.data, many=True)
        if serializer.is_valid():
            timetable = {}
            timeslots = models.Timeslot.objects.all()
            locations = models.Location.objects.prefetch_related(
                Prefetch('room_set', queryset=models.Room.objects.order_by('id')))
            
            for data in serializer.validated_data:
                length = data.get('length', -1)
                preset = data.get('preset', [])
                if length != len(preset):
                    raise ValidationError(f'Property "length" ({length}) is not equal to the actual length of preset ({len(preset)}).')

                # Iterate every lecturer's preset schedule
                for p in preset:
                    room = models.Room.objects.filter(code=p.get('room'))
                    course = models.Course.objects.filter(code=p.get('course'))
                    timeslot = models.Timeslot.objects.filter(code=p.get('timeslot'))

                    # Fetch data if exists in database
                    room = room.get() if room.exists() else None
                    timeslot = timeslot.get() if timeslot.exists() else None

                    # Fetch course data with related classes
                    if course.exists():
                        course = course.prefetch_related(Prefetch('courseclass_set', queryset=models.CourseClass.objects.order_by('id'))).get()
                        neighbors = [p.get('course') for p in preset if p.get('course') != course.code]
                        for course_class in course.courseclass_set.all():
                            timetable[course_class] = {'room': room, 'timeslot': timeslot, 'neighbors': neighbors}

                            # TODO Deal with neighbors
