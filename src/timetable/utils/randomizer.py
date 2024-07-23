"""
FILE: randomizer.py
Randomize dummy timetable data.
"""

class Randomizer:

    def __init__(self,
                 nb_rooms,
                 nb_courses,
                 nb_classes,
                 nb_timeslots,
                 nb_locations,
                 nb_lecturers
                 ):
        """
        Constructor for Randomizer will initialize random instance for the timetable models.
        NOTE Lecturers is denoted by clusters of chosen courses.
        """
        print("Instatiating objects with random value...")
        self.__rooms = ...
        self.__courses = ...
        self.__classes = ...
        self.__timeslots = ...
        self.__locations = ...
        self.__lecturers = ...

    def __generate_rooms(self, nb_rooms):
        pass

    def __generate_courses(self, nb_courses):
        pass

    def __generate_classes(self, nb_classes):
        pass

    def __generate_timeslots(self, nb_timeslots):
        pass

    def __generate_locations(self, nb_locations):
        pass

    def __generate_lecturers(self, nb_lecturers):
        pass

    def get_rooms(self):
        return self.__rooms

    def get_courses(self):
        return self.__courses

    def get_classes(self):
        return self.__classes

    def get_timeslots(self):
        return self.__timeslots

    def get_locations(self):
        return self.__locations

    def get_lecturers(self):
        return self.__lecturers