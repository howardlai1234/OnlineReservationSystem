import pytz
from datetime import datetime
from django.contrib.auth.models import User
from config.models import Timetable

def check_is_staff(user):
    if user.is_staff:
        return True
    return False

def current_phase():
    timetable = Timetable.objects.get()  
    if pytz.UTC.localize(datetime.now()) >= timetable.phase1_start and pytz.UTC.localize(datetime.now()) <= timetable.phase1_end:
        return 1
    if pytz.UTC.localize(datetime.now()) >= timetable.phase2_start and pytz.UTC.localize(datetime.now()) <= timetable.phase2_end:
        return 2
    if pytz.UTC.localize(datetime.now()) >= timetable.phase3_start:
        return 3
    return 0

def base_data(user):
    return {'username': user, 'is_staff': check_is_staff(user), 'phase': current_phase()}