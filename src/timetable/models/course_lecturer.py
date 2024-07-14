from django.db import models
from . import course, lecturer

class CourseLecturer(models.Model):
    course = models.ForeignKey(course.Course, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(lecturer.Lecturer,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.course.code + ' ' + self.lecturer.name