from django.shortcuts import render
from .. import utils

def build(request):
    if request.method == 'POST':
        nb_rooms = int(request.POST['rooms'])
        nb_courses = int(request.POST['courses'])
        nb_classes = int(request.POST['classes'])
        nb_locations = int(request.POST['locations'])
        nb_timeslots = int(request.POST['timeslots'])
        randomizer = utils.Randomizer(nb_rooms,
                                      nb_courses,
                                      nb_classes,
                                      nb_timeslots,
                                      nb_locations) 
        print(randomizer.get_classes())
        print(randomizer.get_rooms())
    return render(request, 'build.html')