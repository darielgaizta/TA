import random
from abc import ABC, abstractmethod
from timetable.models import CourseClass

class TimetableBuilder(ABC):
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
    
    def evaluate(self, timetable: dict, *args, **kwargs) -> int:
        conflict = 0
        class_id = 0

        if kwargs.get('presets'):
            conflict += self.validate_preset(timetable, kwargs.get('presets'))
        
        while class_id < len(self.courses):
            course_class1 = self.courses[class_id]
            neighbor_id = class_id + 1

            # Iterate through all the neighbors
            while neighbor_id < len(self.courses):
                course_class2 = self.courses[neighbor_id]
                conflict += self.validate_neighbor(timetable, course_class1, course_class2)
                neighbor_id += 1
            class_id += 1
        return conflict

    def validate_preset(self, timetable: dict, presets: list[dict]):
        """
        Presets is a list of {Course: {'room': Room, 'timeslot': Timeslot}}
        Searching the `timetable` if all the presets is assigned correctly.
        """
        matches = {}
        for preset in presets:
            course, subdict = list(preset.items())[0]
            found = {k: v for k, v in timetable.items() if k.course == course
                     and any(item in v.items() for item in subdict.items() if item[1] != None)}
            matches = matches | found
        print('Found matches:', matches)
        conflict = len(presets) - len(matches)
        return 0 if conflict <= 0 else conflict

    def validate_neighbor(self, timetable: dict, course_class1: CourseClass, course_class2: CourseClass):
        """
        Validates a class with its neighbor class.
        Searching if a conflict condition is met, returns 1 if there is a conflict.
        """
        room1, timeslot1 = timetable[course_class1].values()
        room2, timeslot2 = timetable[course_class2].values()

        condition1 = (timeslot1 == timeslot2) and (room1 == room2)
        condition2 = (course_class1.course.code == course_class2.course.code) and (timeslot1 != timeslot2)
        condition3 = ((course_class1.number == course_class2.number)
                      and (course_class1.course.code != course_class2.course.code)
                      and room1.location.code != room2.location.code)
        
        is_conflict = condition1 or condition2 or condition3
        return 1 if is_conflict else 0
    
    @abstractmethod
    def run(self, *args, **kwargs) -> tuple[dict, int, int]: pass