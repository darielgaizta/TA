from django.shortcuts import render
from .. import utils

def ui_build(request):
    nb_rooms = 10
    nb_courses = 9
    nb_classes = 3
    nb_timeslots = 10
    nb_locations = 2 
    randomizer = utils.Randomizer(
        nb_rooms,
        nb_courses,
        nb_classes,
        nb_timeslots,
        nb_locations,
        0
    )
    print(randomizer.get_classes())
    print(randomizer.get_rooms())
    return render(request, 'build.html')