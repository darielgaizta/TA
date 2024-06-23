from django.shortcuts import render
from algorithm.genetic import GeneticTimetable
from . import models

def build_all(request):
    rooms = models.Room.objects.all()
    courses = models.Course.objects.all()
    timeslots = models.Timeslot.objects.all()
    
    if request.method == 'POST':
        # Fetch Genetic timetable parameters.
        population_size = request.POST.get("population_size")
        num_generations = request.POST.get("num_generations")

        # Build Genetic timetable.
        timetable = GeneticTimetable(
            rooms=rooms,
            courses=courses,
            timeslots=timeslots,
            population_size=population_size,
            num_generations=num_generations)

        # Run Genetic algorithm.
        solution, conflicts = timetable.run()
        return render(request, 'main/solution.html', {'solution': solution, 'conflicts': conflicts})
    return render(request, 'error/405.html')