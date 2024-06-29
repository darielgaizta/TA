from django.db import models
from . import location

class Room(models.Model):
    """Class that represents room in a campus location."""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField()
    location = models.ForeignKey(location.Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.code + ' ' + self.name