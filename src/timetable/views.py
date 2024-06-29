import time
from django.db.models import Prefetch
from builder.response import ResponseBuilder
from rest_framework.decorators import api_view
from algorithm.genetic import GeneticTimetable
from . import models, utils

@api_view(['GET'])
def build_with_ga(request):
    rooms = models.Room.objects.all()
    courses = models.CourseClass.objects.all()
    timeslots = models.Timeslot.objects.all()
    locations = models.Location.objects.prefetch_related(
        Prefetch('room_set', queryset=models.Room.objects.order_by('id')))

    # Fetch Genetic timetable parameters.
    population_size = int(request.query_params.get("population_size"))
    num_generations = int(request.query_params.get("num_generations"))

    # Build Genetic timetable.
    timetable = GeneticTimetable(
        rooms=rooms,
        courses=courses,
        timeslots=timeslots,
        population_size=population_size,
        num_generations=num_generations)

    # Run Genetic algorithm.
    solution, conflicts = timetable.run()
    
    # Write to database Ms. Excel.
    filename = 'timetable' + str(round(time.time() * 1000))
    xl = utils.Xl(filename=filename)
    xl.setup(locations, timeslots)
    xl.write(solution)

    return ResponseBuilder.respondWithMessage(status=200, message=f'Success with {conflicts} conflicts.')