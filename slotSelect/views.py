from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from ORS.settings import DEBUG
from config.models import Currentphase, Timetable
# Create your views here.

def home(request):
if request.user.is_authenticated:
    phase = Currentphase.objects.get().phase
    allowed_group = Timetable.objects.get().phase1_group_name
    userid = User.objects.get(username=request.user).pk
    group = User.objects.get(username=request.user).groups

    if DEBUG == True:
        phase = 2

    if phase == 2:
        

        return HttpResponse("welcome")
    else:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> You are not allowed to be here, please contact an administrator if you think you should <br> <br><a href="/dashboard">return</a>', status=403)
else:
    return HttpResponse(
        '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)