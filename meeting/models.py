from django.db import models

# Create your models here.


class Useravailability(models.Model):
    # Field name made lowercase.
    userid = models.IntegerField(db_column='userID')
    date = models.DateField()
    # Field name made lowercase.
    slotid = models.IntegerField(db_column='slotID')
