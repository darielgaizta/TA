import random
from timetable.models import CourseClass

class TimetableBuilder:
    """
    Class that builds timetable. Timetable has dimension of (`rooms` x `timeslots`). Each cell 
    in that 2D array are classes that will be filled by `CourseClass` objects from list of courses.

    ### Args:
    - rooms (list): List of `Room` objects.
    - courses (list): List of `CourseClass` objects.
    - timeslots (list): List of `Timeslot` objects.

    ### Attributes:
    - rooms (list): List of `Room` objects.
    - courses (list): List of `CourseClass` objects.
    - timeslots (list): List of `Timeslot` objects.
    - timetable (dict): 2D array of `CourseClass` objects.
    """
    def __init__(self, rooms: list, courses: list, timeslots: list):
        self.rooms = rooms
        self.courses = courses
        self.timeslots = timeslots
        self.timetable = { course: {'room': None, 'timeslot': None} for course in courses }
        self.randomize()
    
    def randomize(self) -> None:
        """
        Generate random timetable.
        """
        for course in self.courses:
            self.timetable[course]['room'] = random.choice(self.rooms)
            self.timetable[course]['timeslot'] = random.choice(self.timeslots)
    
    def evaluate(self, timetable: dict) -> int:
        """
        Calculate fitness score by counting conflicts in a timetable.
        """
        conflicts = 0
        course_id = 0
        while course_id < len(self.courses):
            course_1 = self.courses[course_id]
            comparator_id = course_id + 1
            while comparator_id < len(self.courses):
                course_2 = self.courses[comparator_id]
                if (self.validate(timetable, course_1, course_2)):
                    comparator_id += 1
                    continue
                conflicts += 1
            course_id += 1
        return conflicts
    
    def validate(self, timetable: dict, class_1: CourseClass, class_2: CourseClass) -> bool:
        """
        Returns False if class_1 and class_2 conflict with each other, otherwise returns True.
        """
        room_1, timeslot_1 = timetable[class_1]
        room_2, timeslot_2 = timetable[class_2]

        condition_01 = ((timeslot_1 == timeslot_2) and (room_1 == room_2))
        condition_02 = ((class_1.course.code == class_2.course.code) and (timeslot_1 != timeslot_2))
        condition_03 = (
            (class_1.number == class_2.number)
            and (class_1.course.code != class_2.course.code)
            and (room_1.location.code != room_2.location.code)
        )

        return not (
            condition_01
            or condition_02
            or condition_03
        )