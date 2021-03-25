from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from ORS.settings import DEBUG
from config.models import Currentphase, Timetable
from dashboard.models import Slot
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        phase = Currentphase.objects.get().phase
        allowed_group = Timetable.objects.get().phase2_group_name
        userid = User.objects.get(username=request.user).pk
        group = User.objects.get(username=request.user).groups
        user_allowed_to_access = False
        RegisteredSlotsReturn = []
        grouplist = []

        if DEBUG == True:
            phase = 2

        if phase == 2:
            for gp in request.user.groups.all():
                grouplist.append(gp.name)
                if gp.name == allowed_group:
                    user_allowed_to_access = True
            if user_allowed_to_access == True:
                #request all available slots
                for gp in request.user.groups.all():
                    if Slot.objects.filter(groupid=Group.objects.get(name=gp.name).pk).count() > 0:
                        Registered_slot_of_group = []
                        for s in Slot.objects.filter(groupid=Group.objects.get(name=gp.name).pk).all():
                            Registered_slot_of_group.append({'id': s.slotid, 'start': s.starttime, 'end': s.endtime})
                        RegisteredSlotsReturn.append({'group': gp.name, 'slots': Registered_slot_of_group})


                return render(request, 'selection.html', {
                    'availableTimes': RegisteredSlotsReturn,
                })
            else:
                return HttpResponse(
                    '<h1>ACCEESS DENIED</h1> <br> You are not allowed to be here, please contact an administrator if you think you should <br> <br><a href="/dashboard">return</a>', status=403)
        else:
            return HttpResponse(
                '<h1>ACCEESS DENIED</h1> ', status=403)
    else:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)