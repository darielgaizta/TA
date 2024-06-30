from django.db import models
from . import course

class CourseClass(models.Model):
    """Class that represents course class in university."""
    number = models.IntegerField()
    course = models.ForeignKey(course.Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.course.code + ' ' + self.course.name + '-' + str(self.number)