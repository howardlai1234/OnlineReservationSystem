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
from dashboard.models import Slot, Groupdetail
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

        access_check = check_user_allowed_to_access_phase1(request.user)
        if access_check['flag'] == True:
            grouplist = access_check['grouplist']
            context = {}
            if DEBUG == True:
                print("user allowed to access")
                print("user Group in return list:", grouplist)

            # read registered slot

            for gp in request.user.groups.all():

                #groupid = Group.objects.get(name=gp.name).pk
                if Slot.objects.filter(groupid=Group.objects.get(
                        name=gp.name).pk).count() > 0:
                    Registered_slot_of_group = []
                    for s in Slot.objects.filter(
                            groupid=Group.objects.get(name=gp.name).pk).all():
                        Registered_slot_of_group.append(
                            {'id': s.slotid, 'start': s.starttime, 'end': s.endtime})
                    RegisteredSlotsReturn.append(
                        {'group': gp.name, 'slots': Registered_slot_of_group})

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
                    period_start_str = period_start.strftime(
                        "%Y/%m/%d %H:%M:%S")
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
                print(form)

            if form.is_valid():
                userid = User.objects.get(username=request.user).pk
                group = User.objects.get(username=request.user).groups

                for gp in request.user.groups.all():
                    if gp.name == allowed_group:
                        user_allowed_to_access = True
                    if gp.name == form.cleaned_data['confirm_group']:
                        user_in_target_group = True

                if user_allowed_to_access == True and user_in_target_group == True:
                    startTime = datetime.datetime.strptime(
                        form.cleaned_data['confirm_startTime'], '%Y/%m/%d %H:%M:%S')
                    group = form.cleaned_data['confirm_group']
                    meetingLen = form.cleaned_data['confirm_duration']
                    numberOfMeet = form.cleaned_data["confirm_no_of_meeting"]

                    period_end = startTime

                    for i in range(0, numberOfMeet):
                        session_start = period_end
                        period_end = period_end + \
                            datetime.timedelta(minutes=meetingLen)
                        Slot.objects.create(
                            ownerid=userid,
                            starttime=session_start,
                            endtime=period_end,
                            groupid=Group.objects.get(name=group).pk
                        )

                    return HttpResponseRedirect('/calendar/')
                else:
                    return HttpResponse(
                        '<h1>Unauthorised Access</h1>', status=403)
            else:
                return HttpResponse('<h1>Invalid Form</h1>', status=404)
        else:
            return HttpResponse('<h1>ACCEESS DENIED</h1>', status=404)
    else:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)

def remove(request):
    if request.user.is_authenticated:
        userid = User.objects.get(username=request.user).pk
        group = User.objects.get(username=request.user).groups
        grouplist = []
        user_allowed_to_access = False
        # For Debug Function
        if DEBUG == True:
            phase = 1
        access_check = check_user_allowed_to_access_phase1(request.user)
        if access_check['flag'] == True:
            grouplist = access_check['grouplist']
        
    else:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)

def setMinSlot(request):
    if request.user.is_authenticated:
        userid = User.objects.get(username=request.user).pk
        group = User.objects.get(username=request.user).groups
        grouplist = []
        miniumSlotReturn = []
        formError = ''
        formSuccess = ''

        access_check = check_user_allowed_to_access_phase1(request.user)
        if access_check['flag'] == True:
            grouplist = access_check['grouplist']
            if request.method == 'POST':
                form = forms.ChangeMinRequired(request.POST)
                if form.is_valid():
                    if form.cleaned_data['minrequiredslot'] <= Slot.objects.filter(groupid=Group.objects.get(name=form.cleaned_data['groupname']).pk).count():
                        Groupdetail.objects.filter(groupid=Group.objects.get(name=form.cleaned_data['groupname']).pk).update(min_required_slot=form.cleaned_data['minrequiredslot'])
                        formSuccess = 'SUCCESS: Minunum required slot has been updated'

                    else:
                        formError = 'ERROR: The Mininum required slot exceed the provided number of slots, please reduce the number.'
            for gp in grouplist:
                groupID = Group.objects.get(name=gp).pk
                if Groupdetail.objects.filter(groupid=groupID).count() == 0:
                    Groupdetail.objects.create(
                        groupid=groupID, 
                        min_required_slot=5 
                    )
                    miniumSlotReturn.append({'groupname': gp, 'minslot': 5})
                else:
                    gpDetail = Groupdetail.objects.filter(groupid=groupID).get()
                    miniumSlotReturn.append({'groupname': gp, 'minslot': gpDetail.min_required_slot})

            return render(request, 'calendar/setmin.html', {
                'formError': formError,
                'formSuccess': formSuccess,
                'miniumSlotReturn': miniumSlotReturn
            })
                
    else:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)


def check_user_allowed_to_access_phase1(user):
    user_allowed_to_access = False
    allowed_group = Timetable.objects.get().phase1_group_name
    phase = -1
    grouplist = []
    if DEBUG == True:
        phase = 1

    for gp in user.groups.all():
        grouplist.append(gp.name) 
        if gp.name == allowed_group:
            user_allowed_to_access = True

    if phase == 1 and user_allowed_to_access == True:
        return {'flag': True, 'grouplist': grouplist}
    else:
        return {'flag': False, 'grouplist': grouplist}

    
