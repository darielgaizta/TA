import time
from django.shortcuts import render
from algorithm.runner import Runner
from .. import utils

def build(request):
    context = {}
    if request.method == 'POST':
        nb_rooms = int(request.POST['rooms'])
        nb_courses = int(request.POST['courses'])
        nb_classes = int(request.POST['classes'])
        nb_locations = int(request.POST['locations'])
        nb_timeslots = int(request.POST['timeslots'])
        search_space = int(request.POST['search_space'])
        iterations = int(request.POST['iterations'])
        algorithm = request.POST['algorithm']

        data = utils.Randomizer(
            nb_rooms,
            nb_courses,
            nb_classes,
            nb_timeslots,
            nb_locations,
        )

        if algorithm == 'ga':
            solution, conflict,time_taken = Runner.run_genetic(
                rooms=data.get_rooms(),
                courses=data.get_classes(),
                timeslots=data.get_timeslots(),
                population_size=search_space,
                num_generations=iterations
            )
        elif algorithm == 'ts':
            solution, conflict, time_taken = Runner.run_tabu_search(
                rooms=data.get_rooms(),
                courses=data.get_classes(),
                timeslots=data.get_timeslots(),
                tabu_list_size=search_space,
                max_iterations=iterations
            )
        else: raise Exception('Invalid algorithm.')

        # Write to Excel
        filename = 'timetable_' + str(round(time.time() * 1000))
        xl = utils.Xl(filename=filename)
        xl.setup(data.get_timeslots(), rooms=data.get_rooms())
        xl.write(solution)
        
        context = {
            'time_taken': time_taken,
            'solution': solution,
            'conflict': conflict,
            'nb_rooms': nb_rooms,
            'nb_courses': nb_courses,
            'nb_classes': nb_classes,
            'nb_timeslots': nb_timeslots,
            'nb_locations': nb_locations,
            'search_space': search_space,
            'iterations': iterations,
            'algorithm': algorithm
        }
         
    return render(request, 'build.html', context)