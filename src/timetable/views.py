import time
from django.db.models import Prefetch
from builder.response import ResponseBuilder
from rest_framework.decorators import api_view
from algorithm.runner import Runner
from . import models, utils

def build(runner, *args, **kwargs):
    """
    Base timetable view. Processed input will be processed to Ms. Excel
    and user will get a message with number of conflicts as a response.
    """
    timeslots = models.Timeslot.objects.all()
    locations = models.Location.objects.prefetch_related(
        Prefetch('room_set', queryset=models.Room.objects.order_by('id')))
    
    # Run algorithm.
    solution, conflicts = runner(*args, **kwargs)

    # Write to database Ms. Excel.
    filename = 'timetable' + str(round(time.time() * 1000))
    xl = utils.Xl(filename=filename)
    xl.setup(locations, timeslots)
    xl.write(solution)
    return ResponseBuilder.respondWithMessage(status=200, message=f'Success with {conflicts} conflicts.')

@api_view(['GET'])
def build_with_ga(request):
    rooms = models.Room.objects.all()
    courses = models.CourseClass.objects.all()
    timeslots = models.Timeslot.objects.all()

    # Fetch Genetic timetable parameters.
    population_size = int(request.query_params.get("population_size"))
    num_generations = int(request.query_params.get("num_generations"))

    return build(runner=Runner.run_genetic,
        rooms=rooms,
        courses=courses,
        timeslots=timeslots,
        population_size=population_size,
        num_generations=num_generations)

@api_view(['GET'])
def build_with_ts(request):
    rooms = models.Room.objects.all()
    courses = models.CourseClass.objects.all()
    timeslots = models.Timeslot.objects.all()

    # Fetch Tabu Search parameters.
    tabu_list_size = int(request.query_params.get("tabu_list_size"))
    max_iterations = int(request.query_params.get("max_iterations"))

    return build(runner=Runner.run_tabu_search,
        rooms=rooms,
        courses=courses,
        timeslots=timeslots,
        tabu_list_size=tabu_list_size,
        max_iterations=max_iterations)