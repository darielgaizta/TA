"""
Custom view is a view for handling user requests.
In this usage, user might want to custom their schedule preference on timetable.
"""
import time
from django.db.models import Prefetch
from rest_framework.decorators import api_view
from builder.response import ResponseBuilder
from algorithm.runner import Runner
from .. import models, serializers, utils

def preset(request, runner, *args, **kwargs):
    if request.method == 'POST':
        serializer = serializers.PresetSerializer(data=request.data, many=True)
        if serializer.is_valid():
            timeslots = models.Timeslot.objects.all()
            locations = models.Location.objects.prefetch_related(
                Prefetch('room_set', queryset=models.Room.objects.order_by('id')))
            
            presets = []
            
            for data in serializer.validated_data:

                # Search data in database
                room = models.Room.objects.filter(code=data.get('room'))
                course = models.Course.objects.filter(code=data.get('course'))
                timeslot = models.Timeslot.objects.filter(code=data.get('timeslot'))
                
                # Fetch data if exists in database
                room = room.get() if room.exists() else None
                timeslot = timeslot.get() if timeslot.exists() else None

                # Fetch course data with related classes
                if course.exists():
                    presets.append({course.get(): {'room': room, 'timeslot': timeslot}})
            
            print('Received preset:', presets)
            solution, conflicts = runner(*args, **kwargs, presets=presets)

            # Write to database Ms. Excel.
            filename = 'timetable' + str(round(time.time() * 1000))
            xl = utils.Xl(filename=filename)
            xl.setup(timeslots, locations=locations)
            xl.write(solution)
            return ResponseBuilder.respondWithMessage(status=200, message=f'Success with {conflicts} conflicts.')
        return ResponseBuilder.respondWithMessage(400, serializer.errors)

@api_view(['POST'])
def preset_with_ga(request):
    rooms = models.Room.objects.all()
    courses = models.CourseClass.objects.all()
    timeslots = models.Timeslot.objects.all()

    # Fetch Genetic timetable parameters.
    population_size = int(request.query_params.get("population_size"))
    num_generations = int(request.query_params.get("num_generations"))

    return preset(
        request,
        runner=Runner.run_genetic,
        rooms=rooms,
        courses=courses,
        timeslots=timeslots,
        population_size=population_size,
        num_generations=num_generations)

@api_view(['POST'])
def preset_with_ts(request):
    rooms = models.Room.objects.all()
    courses = models.CourseClass.objects.all()
    timeslots = models.Timeslot.objects.all()

    # Fetch Tabu Search parameters.
    tabu_list_size = int(request.query_params.get("tabu_list_size"))
    max_iterations = int(request.query_params.get("max_iterations"))

    return preset(
        request,
        runner=Runner.run_tabu_search,
        rooms=rooms,
        courses=courses,
        timeslots=timeslots,
        tabu_list_size=tabu_list_size,
        max_iterations=max_iterations)

def fake_preset():
    # TODO Randomize data based on a given range.
    pass