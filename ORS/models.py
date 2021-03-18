# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Gp(models.Model):
    groupid = models.AutoField(db_column='groupID', primary_key=True)  # Field name made lowercase.
    groupname = models.CharField(db_column='groupName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    groupownerid = models.IntegerField(db_column='groupOwnerID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'gp'


class Groupmember(models.Model):
    groupid = models.IntegerField(db_column='groupID')  # Field name made lowercase.
    memberid = models.IntegerField(db_column='memberID')  # Field name made lowercase.
    joindate = models.DateTimeField(db_column='joinDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'groupmember'


class Meeting(models.Model):
    # Field name made lowercase.
    meetingid = models.AutoField(db_column='meetingID', primary_key=True)
    # Field name made lowercase.
    hostid = models.IntegerField(db_column='hostID')
    # Field name made lowercase.
    participantid = models.IntegerField(db_column='participantID')
    date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    # Field name made lowercase.
    statusid = models.IntegerField(db_column='statusID', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meeting'


class Message(models.Model):
    messageid = models.AutoField(db_column='messageID', primary_key=True)  # Field name made lowercase.
    senderid = models.IntegerField(db_column='senderID')  # Field name made lowercase.
    receiverid = models.IntegerField(db_column='receiverID')  # Field name made lowercase.
    referenceid = models.IntegerField(db_column='referenceID', blank=True, null=True)  # Field name made lowercase.
    sendtime = models.DateTimeField(db_column='sendTime', blank=True, null=True)  # Field name made lowercase.
    viewed = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    body = models.CharField(max_length=4096, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message'


class Slot(models.Model):
    slotid = models.AutoField(db_column='slotID', primary_key=True)  # Field name made lowercase.
    ownerid = models.IntegerField(db_column='ownerID')  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='startTime')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='endTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'slot'


class Slotsopento(models.Model):
    slotsid = models.IntegerField(db_column='slotsID')  # Field name made lowercase.
    isgroup = models.IntegerField(db_column='isGroup', blank=True, null=True)  # Field name made lowercase.
    opentoid = models.IntegerField(db_column='OpenToID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'slotsopento'


class User(models.Model):
    # Field name made lowercase.
    userid = models.AutoField(db_column='userID', primary_key=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    # Field name made lowercase.
    firstname = models.CharField(
        db_column='firstName', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    lastname = models.CharField(
        db_column='lastName', max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=255, blank=True, null=True)
    # Field name made lowercase.
    typeid = models.CharField(
        db_column='typeID', max_length=255, blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    # Field name made lowercase.
    hashpw = models.CharField(
        db_column='hashPW', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Useravailability(models.Model):
    # Field name made lowercase.
    userid = models.IntegerField(db_column='userID')
    date = models.DateField()
    # Field name made lowercase.
    slotid = models.IntegerField(db_column='slotID')

    class Meta:
        managed = False
        db_table = 'useravailability'
