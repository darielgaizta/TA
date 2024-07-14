"""
Author: Dariel Gaizta
File engine.py is the main part of this application. It contains several functions that take user's input,
import internal modules, and process them to generate timetable.
"""

import random
import string
from timetable import models

class Engine:
    def __generate_rooms(self, n: int, locations: list):
        """Generate n Room objects."""
        rooms = []
        for _ in range(n):
            room = models.Room(
                name=self.__get_random_string(50),
                code=self.__get_random_string(10),
                capacity=random.randint(1, 100),
                location=random.choice(locations)
            )
            rooms.append(room)
        return rooms

    def __generate_courses(self, n: int):
        """Generate n Course objects."""
        courses = []
        for _ in range(n):
            course = models.Course(
                name=self.__get_random_string(50),
                code=self.__get_random_string(10),
                credit=random.randint(1, 5),
                semester=random.choice([1, 3, 5, 7]),
                department=self.__get_random_string(50)
            )
            courses.append(course)
        return courses

    def __generate_timeslots(self, n: int):
        """Generate n Timeslot objects."""
        timeslots = []
        for _ in range(n):
            timeslot = models.Timeslot(
                code=self.__get_random_string(10)
            )
            timeslots.append(timeslot)
        return timeslots
    
    def __generate_locations(self, n: int):
        """Generate n Location objects."""
        locations = []
        for _ in range(n):
            location = models.Location(
                name=self.__get_random_string(50),
                code=self.__get_random_string(10)
            )
            locations.append(location)
        return locations
        
    def __generate_lecturers(self, n: int):
        """Generate n Lecturer objects."""
        lecturers = []
        for _ in range(n):
            lecturer = models.Lecturer(
                name=self.__get_random_string(50)
            )
            lecturers.append(lecturer)
        return lecturers

    def __generate_course_classes(self, n_max: int, courses: list):
        """Generate [n_min..n_max] CourseClass objects for each Course."""
        course_classes = []
        for course in courses:
            for n in range(1, (n_max + 1)):
                course_class = models.CourseClass(
                    number=n,
                    course=course
                )
                course_classes.append(course_class)
        return course_classes

    def __get_random_string(length: int):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))
