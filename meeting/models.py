from django.db import models

# Create your models here.

class Useravailability(models.Model):
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    date = models.DateField()
    slotid = models.IntegerField(db_column='slotID')  # Field name made lowercase.
