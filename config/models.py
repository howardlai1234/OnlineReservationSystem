from django.db import models

# Create your models here.


class Timetable(models.Model):
    phase1_start = models.DateTimeField()
    phase1_end = models.DateTimeField()
    phase1_group_name = models.CharField(max_length=150)
    phase2_start = models.DateTimeField()
    phase2_end = models.DateTimeField()
    phase2_group_name = models.CharField(max_length=150)
    phase3_start = models.DateTimeField()


class Currentphase(models.Model):
    phase = models.IntegerField()
