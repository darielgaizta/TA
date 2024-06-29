from django.db import models

class Course(models.Model):
    """Class that represents course in university."""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    credit = models.IntegerField()
    semester = models.IntegerField()
    department = models.CharField(max_length=50)

    def __str__(self):
        return self.code + ' ' + self.name