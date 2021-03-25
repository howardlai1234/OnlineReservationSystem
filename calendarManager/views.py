import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import connections
from django.db.utils import OperationalError
from ORS.settings import DEBUG
from django.contrib.auth.models import User, Group
from config.models import Currentphase, Timetable
from calendarManager import forms
from dashboard.models import Slot
#from django.contrib.auth.models import Group

# Create your views here.


def home(request):
    print("celander:", Group.objects.all())
    phase = Currentphase.objects.get().phase
    allowed_group = Timetable.objects.get().phase1_group_name
    user_allowed_to_access = 0
    grouplist = []
    computed_detail = {'not_empty': False}

    
    RegisteredSlotsReturn = []
    period_start = {}
    period_end = {}
    meetingLen = 0
    numberOfMeet = 0
    period_start_str = ''

    if request.user.is_authenticated:
        userid = User.objects.get(username=request.user).pk
        group = User.objects.get(username=request.user).groups
        # For Debug Function
        if DEBUG == True:
            phase = 1
            print("userid: ", userid)
        for gp in request.user.groups.all():
            grouplist.append(gp.name)
            if gp.name == allowed_group:
                user_allowed_to_access = 1
                print("Group of user: ", request.user, ":", gp.name)


        if phase == 1 and user_allowed_to_access == 1:
            context = {}
            if DEBUG == True:
                print("user allowed to access")
                print("user Group in return list:", grouplist)

            #read registered slot

            for gp in request.user.groups.all():

                #groupid = Group.objects.get(name=gp.name).pk
                if Slot.objects.filter(groupid=Group.objects.get(name=gp.name).pk).count() > 0:
                    Registered_slot_of_group = []
                    for s in Slot.objects.filter(groupid=Group.objects.get(name=gp.name).pk).all():
                        Registered_slot_of_group.append({'id': s.slotid, 'start': s.starttime, 'end': s.endtime})
                    RegisteredSlotsReturn.append({'group': gp.name, 'slots': Registered_slot_of_group})

            # form handling
            if request.method == 'POST':
                form = forms.NameForm(request.POST)
                context['form'] = forms
                if form.is_valid():
                    # debug information
                    if DEBUG == True:
                        print("Form valid: ", form)
                        print(
                            "StartHour: ", int(
                                form.cleaned_data['startHour']))
                        print(
                            "StartMinute: ",
                            form.cleaned_data['startMinute'])
                        print(
                            "Meeting Length: ",
                            form.cleaned_data['meetingLength'])
                        print(
                            "Number of Meeting: ",
                            form.cleaned_data['numberOfMeeting'])

                    # convert data from form into correct and esaily to
                    # understand variables
                    date = form.cleaned_data['date']
                    startHr = int(form.cleaned_data['startHour'])
                    startMin = int(form.cleaned_data['startMinute'])
                    meetingLen = int(form.cleaned_data['meetingLength'])
                    numberOfMeet = int(form.cleaned_data["numberOfMeeting"])
                    period_start = datetime.datetime(
                        date.year, date.month, date.day, startHr, startMin, 0)
                    meetingSession = []
                    period_start_str = period_start.strftime("%Y/%m/%d %H:%M:%S")
                    period_end = period_start
                    for i in range(0, numberOfMeet):
                        session_start = period_end
                        period_end = period_end + \
                            datetime.timedelta(minutes=meetingLen)
                        meetingSession.append(
                            {'startTime': session_start, 'endTime': period_end})

                    if DEBUG == True:
                        print(period_start)
                        print(period_end)
                        for x in meetingSession:
                            print(
                                " start:", x['startTime'], "end:", x['endTime'])
                else:
                    computed_detail = {'not_empty': False}
                # prepare the checking
                computed_detail = {
                    'not_empty': True,
                    'group': form.cleaned_data['group'],
                    'startTime_str': period_start_str,
                    'startTime': period_start,
                    'endTime': period_end,
                    'duration': meetingLen,
                    'no_of_meeting': numberOfMeet}

            return render(request, 'calendar.html', {
                'confirmForm': forms.ConfirmForm,
                'group_list': grouplist,
                'username': request.user,
                'availableTimes': RegisteredSlotsReturn,
                'computed_details': computed_detail
            })
        else:
            return HttpResponse(
                '<h1>ACCEESS DENIED</h1> <br> You are not allowed to be here, please contact an administrator if you think you should <br> <br><a href="/dashboard">return</a>', status=403)
    else:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)


def confirm(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            allowed_group = Timetable.objects.get().phase1_group_name 
            form = forms.ConfirmForm(request.POST)
            user_allowed_to_access = False
            user_in_target_group = False

            if DEBUG == True:
                print (form)

            if form.is_valid():
                userid = User.objects.get(username=request.user).pk
                group = User.objects.get(username=request.user).groups

                for gp in request.user.groups.all():
                    if gp.name == allowed_group:
                        user_allowed_to_access = True
                    if gp.name == form.cleaned_data['confirm_group']:
                        user_in_target_group = True

                if user_allowed_to_access == True and user_in_target_group == True:
                    startTime = datetime.datetime.strptime(form.cleaned_data['confirm_startTime'], '%Y/%m/%d %H:%M:%S')
                    group = form.cleaned_data['confirm_group']
                    meetingLen = form.cleaned_data['confirm_duration']
                    numberOfMeet = form.cleaned_data["confirm_no_of_meeting"]

                    period_end = startTime

                    for i in range(0, numberOfMeet):
                        session_start = period_end
                        period_end = period_end + \
                            datetime.timedelta(minutes=meetingLen)
                        Slot.objects.create(
                            ownerid = userid,
                            starttime = session_start,
                            endtime = period_end,
                            groupid = Group.objects.get(name=group).pk
                        )
 
                    return HttpResponseRedirect('/calendar/')
                else:
                    return HttpResponse('<h1>Unauthorised Access</h1>', status=403)
            else:
                return HttpResponse('<h1>Invalid Form</h1>', status=404)
        else: 
            return HttpResponse('<h1>ACCEESS DENIED</h1>', status=404)
    else:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)