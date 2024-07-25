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
    print('----Classes\n', randomizer.get_classes())
    print('----Locations\n', randomizer.get_locations())
    print('----Rooms\n', randomizer.get_rooms())
    print('----Timeslots\n', randomizer.get_timeslots())
    for room in randomizer.get_rooms():
        print(room, '---->', room.location)
    return render(request, 'build.html')