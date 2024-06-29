import time
from builder.response import ResponseBuilder
from rest_framework.decorators import api_view
from algorithm.genetic import GeneticTimetable
from . import models, utils

@api_view(['POST'])
def build_all(request):
    if request.method == 'POST':
        rooms = models.Room.objects.all()
        courses = models.CourseClass.objects.all()
        timeslots = models.Timeslot.objects.all()

        # Fetch Genetic timetable parameters.
        population_size = request.data.get("population_size")
        num_generations = request.data.get("num_generations")

        # Build Genetic timetable.
        timetable = GeneticTimetable(
            rooms=rooms,
            courses=courses,
            timeslots=timeslots,
            population_size=population_size,
            num_generations=num_generations)

        # Run Genetic algorithm.
        solution, conflicts = timetable.run()
        
        # Write to database Ms. Excel or Google Sheets.
        filename = 'timetable' + str(round(time.time() * 1000))
        utils.write_xl(filename=filename, content=solution)

        return ResponseBuilder.respondWithMessage(status=200, message=f'Success with {conflicts} conflicts.')