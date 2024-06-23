from django.contrib import admin
from . import models

admin.site.register(models.Course)
admin.site.register(models.CourseClass)
admin.site.register(models.Location)
admin.site.register(models.Room)
admin.site.register(models.Timeslot)