from django.db import models

class Timeslot(models.Model):
    """Class that represents time slot in university."""
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.code