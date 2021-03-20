from django.db import models

# Create your models here.


# class Meeting(models.Model):
#     # Field name made lowercase.
#     meetingid = models.AutoField(db_column='meetingID', primary_key=True)
#     # Field name made lowercase.
#     hostid = models.IntegerField(db_column='hostID')
#     # Field name made lowercase.
#     participantid = models.IntegerField(db_column='participantID')
#     date = models.DateField(blank=True, null=True)
#     name = models.CharField(max_length=255, blank=True, null=True)
#     remark = models.CharField(max_length=255, blank=True, null=True)
#     # Field name made lowercase.
#     statusid = models.IntegerField(db_column='statusID', blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'meeting'


# class User(models.Model):
#     # Field name made lowercase.
#     userid = models.AutoField(db_column='userID', primary_key=True)
#     # Field name made lowercase.
#     firstname = models.CharField(
#         db_column='firstName', max_length=255, blank=True, null=True)
#     lastname = models.CharField(max_length=255, blank=True, null=True)
#     email = models.CharField(max_length=255, blank=True, null=True)
#     tel = models.CharField(max_length=255, blank=True, null=True)
#     # Field name made lowercase.
#     typeid = models.CharField(
#         db_column='typeID', max_length=255, blank=True, null=True)
#     active = models.IntegerField(blank=True, null=True)
#     # Field name made lowercase.
#     hashpw = models.CharField(
#         db_column='hashPW', max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'user'
