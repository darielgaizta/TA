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
        self.preset = None
    
    def randomize(self) -> None:
        """
        Generate random timetable.
        """
        for course in self.courses:
            self.timetable[course]['room'] = random.choice(self.rooms)
            self.timetable[course]['timeslot'] = random.choice(self.timeslots)
    
    def evaluate(self, timetable: dict, *args, **kwargs) -> int:
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
                if not self.__validate_class(timetable, course_1, course_2):
                    conflicts += 1
                comparator_id += 1
            course_id += 1
        if kwargs.get('preset'):
            _, preset_conflict = self.__validate_preset(kwargs.get('total_preset_course'), timetable, kwargs.get('preset'))
            conflicts += preset_conflict
        return conflicts
    
    def __validate_class(self, timetable: dict, class_1: CourseClass, class_2: CourseClass) -> bool:
        """
        Returns True if class_1 and class_2 conflict with each other, otherwise returns False.
        -> True: means conflict found.
        -> False: means there is no conflict.
        """
        room_1, timeslot_1 = timetable[class_1].values()
        room_2, timeslot_2 = timetable[class_2].values()

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
    
    def __match_preset(self, timetable: dict, preset: dict):
        """Search preset classes in timetable"""
        result = {}
        for course_class, subdict in preset.items():
            is_match = all(item in timetable[course_class].items() for item in subdict.items() if item[1] != None)
            if is_match: result[course_class] = timetable[course_class]
        return result
    
    def __validate_preset(self, total_preset_course: int, timetable: dict, preset: dict):
        matched = self.__match_preset(timetable, preset)
        conflicts = total_preset_course - len(matched)
        return matched, conflicts
    
    @abstractmethod
    def run(self, *args, **kwargs) -> tuple[dict, int]: pass