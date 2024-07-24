"""
FILE: randomizer.py
Randomize dummy timetable data.
"""

import random
import string
from faker import Faker
from .. import models

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
        print("Instantiating objects with random value...")
        self.__faker = Faker()
        self.__rooms = []
        self.__courses = []
        self.__classes = []
        self.__timeslots = []
        self.__locations = []
        self.__lecturers = []
        self.__generate_rooms(nb_rooms, nb_locations)
        self.__generate_classes(nb_classes, nb_courses)
        self.__generate_timeslots(nb_timeslots)

    def __generate_rooms(self, nb_rooms, nb_locations):
        self.__generate_locations(nb_locations)
        for _ in range(nb_rooms):
            name = self.__faker.name()
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            capacity = random.randint(10, 100)
            location = random.choice(self.__locations)
            new_room = models.Room.objects.create(
                name=name,
                code=code,
                capacity=capacity,
                location=location
            )
            self.__rooms.append(new_room)

    def __generate_courses(self, nb_courses):
        for _ in range(nb_courses):
            name = self.__faker.name()
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            credit = random.randint(2, 5)
            semester = random.randint(1, 4)
            department = self.__faker.name()
            new_courses = models.Course.objects.create(
                name=name,
                code=code,
                credit=credit,
                semester=semester,
                department=department
            )
            self.__courses.append(new_courses)

    def __generate_classes(self, nb_classes, nb_courses):
        self.__generate_courses(nb_courses)
        for course in self.__courses:
            n = random.randint(1, nb_classes)
            for i in range(1, n + 1):
                new_course_class = models.CourseClass.objects.create(
                    number=i,
                    course=course
                )
                self.__classes.append(new_course_class)

    def __generate_timeslots(self, nb_timeslots):
        for _ in range(nb_timeslots):
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            new_timeslot = models.Timeslot.objects.create(code=code)
            self.__timeslots.append(new_timeslot)

    def __generate_locations(self, nb_locations):
        for _ in range(nb_locations):
            name = self.__faker.name()
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            new_location = models.Location.objects.create(name=name, code=code)
            self.__locations.append(new_location)

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