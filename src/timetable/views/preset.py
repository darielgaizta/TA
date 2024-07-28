import time
from django.shortcuts import render
from algorithm.runner import Runner
from .. import utils

def preset(request):
    context = {}
    if request.method == 'POST':
        filename = 'timetable_' + str(round(time.time() * 1000))
        nb_rooms = int(request.POST['rooms'])
        nb_courses = int(request.POST['courses'])
        nb_classes = int(request.POST['classes'])
        nb_locations = int(request.POST['locations'])
        nb_timeslots = int(request.POST['timeslots'])
        search_space = int(request.POST['search_space'])
        iterations = int(request.POST['iterations'])
        algorithm = request.POST['algorithm']
        only_room = int(request.POST.get('only_room', 0))
        only_timeslot = int(request.POST.get('only_timeslot', 0))
        both_room_timeslot = int(request.POST.get('both_room_timeslot', 0))

        data = utils.Randomizer(
            nb_rooms,
            nb_courses,
            nb_classes,
            nb_timeslots,
            nb_locations,
            only_room,
            only_timeslot,
            both_room_timeslot,
        )

        if algorithm == 'ga':
            solution, conflict,time_taken = Runner.run_genetic(
                rooms=data.get_rooms(),
                courses=data.get_classes(),
                timeslots=data.get_timeslots(),
                population_size=search_space,
                num_generations=iterations,
                presets=data.get_presets()
            )
        elif algorithm == 'ts':
            solution, conflict, time_taken = Runner.run_tabu_search(
                rooms=data.get_rooms(),
                courses=data.get_classes(),
                timeslots=data.get_timeslots(),
                tabu_list_size=search_space,
                max_iterations=iterations,
                presets=data.get_presets()
            )
        else: raise Exception('Invalid algorithm.')

        context = {
            'filename': filename,
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
            'algorithm': algorithm,
            'only_room': only_room,
            'only_timeslot': only_timeslot,
            'both_room_timeslot': both_room_timeslot
        }

        # Write to Excel
        xl = utils.Xl(filename=filename)
        xl.setup(data.get_timeslots(), rooms=data.get_rooms())
        xl.write(solution)

        # Write to YAML
        yml = utils.Yml(filename=filename)
        yml.write(content=context)

    return render(request, 'preset.html', context)