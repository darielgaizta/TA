from django.db import models

class Location(models.Model):
    """Class that represents campus location in university."""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.code + ' ' + self.name