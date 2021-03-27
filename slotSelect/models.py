from django.db import models

# Create your models here.

class Selection(models.Model):
    groupid = models.IntegerField()
    userid = models.IntegerField()
    userorder = models.IntegerField()