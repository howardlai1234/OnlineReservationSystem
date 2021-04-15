##from django.db import models

# Create your models here.


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or
# field names.
from django.db import models


class Groupdetail(models.Model):
    groupid = models.IntegerField()
    min_required_slot = models.IntegerField()


class Meeting(models.Model):
    # Field name made lowercase.
    meetingid = models.AutoField(db_column='meetingID', primary_key=True)
    # Field name made lowercase.
    hostid = models.IntegerField(db_column='hostID')
    # Field name made lowercase.
    participantid = models.IntegerField(db_column='participantID')
    date = models.DateField(blank=True, null=True)
    starttime = models.TimeField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    # Field name made lowercase.
    statusid = models.IntegerField(db_column='statusID', blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'meeting'


class Message(models.Model):
    # Field name made lowercase.
    messageid = models.AutoField(db_column='messageID', primary_key=True)
    # Field name made lowercase.
    senderid = models.IntegerField(db_column='senderID')
    # Field name made lowercase.
    receiverid = models.IntegerField(db_column='receiverID')
    # Field name made lowercase.
    referenceid = models.IntegerField(
        db_column='referenceID', blank=True, null=True)
    # Field name made lowercase.
    meetingid = models.IntegerField()
    sendtime = models.DateTimeField(
        db_column='sendTime', blank=True, null=True)
    viewed = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    body = models.CharField(max_length=4096, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'message'


class Slot(models.Model):
    # Field name made lowercase.
    slotid = models.AutoField(db_column='slotID', primary_key=True)
    # Field name made lowercase.
    ownerid = models.IntegerField(db_column='ownerID')
    # Field name made lowercase.
    starttime = models.DateTimeField(db_column='startTime')
    # Field name made lowercase.
    endtime = models.DateTimeField(db_column='endTime')
    groupid = models.IntegerField(db_column='groupID')
    active = models.BooleanField()

    class Meta:
        #managed = False
        db_table = 'slot'
