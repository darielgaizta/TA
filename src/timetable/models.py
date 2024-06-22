from django.db import models

class Course(models.Model):
    """Class that represents course in university."""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5, unique=True)
    credit = models.IntegerField()
    semester = models.IntegerField()
    department = models.CharField(max_length=50)

    def __str__(self):
        return self.code
    

class CourseClass(models.Model):
    """Class that represents course class in university."""
    number = models.IntergerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.course.code + '-' + str(self.number)


class Location(models.Model):
    """Class that represents campus location in university."""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.code


class Room(models.Model):
    """Class that represents room in a campus location."""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5, unique=True)
    capacity = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.code


class Timeslot(models.Model):
    """Class that represents time slot in university."""
    code = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.code