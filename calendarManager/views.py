import datetime
import pytz
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from ORS.function import base_data
from ORS.settings import DEBUG
from config.models import Currentphase, Timetable
from calendarManager import forms
from dashboard.models import Slot, Groupdetail

# Create your views here.


def home(request):
    print("celander:", Group.objects.all())
    phase = 0
    #allowed_group = Timetable.objects.get().phase1_group_name
    #user_allowed_to_access = 0
    grouplist = []
    computed_detail = {'not_empty': False}

    RegisteredSlotsReturn = []
    period_start = {}
    period_end = {}
    meetingLen = 0
    numberOfMeet = 0
    period_start_str = ''

    # for time collosion checking
    timecollision = False
    formError = ''

    if not request.user.is_authenticated:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)
            
    userid = User.objects.get(username=request.user).pk
    base_return = base_data(request.user)
    phase = base_return['phase']
    #group = User.objects.get(username=request.user).groups
    if DEBUG:
        phase = 1


    access_check = check_user_allowed_to_access_phase1(request.user)
    if not access_check['flag']:
         return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> You are not allowed to be here, please contact an administrator if you think you should <br> <br><a href="/dashboard">return</a>', status=403)

    if not phase == 1:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> This feature is not available now, please check the scheudule<br><a href="/dashboard">return</a>', status=403)   
             
    grouplist = access_check['grouplist']
    context = {}
    if DEBUG:
        print("user allowed to access")
        print("user Group in return list:", grouplist)

    # read registered slot

    for gp in request.user.groups.all():

        #groupid = Group.objects.get(name=gp.name).pk
        if Slot.objects.filter(groupid=Group.objects.get(
                name=gp.name).pk).count() > 0:
            number_Of_Group_Member = getGroupMemberCount(gp.name)
            slot_counter = 0
            if DEBUG:
                print(
                    "Number of Group Member :",
                    number_Of_Group_Member)
            Registered_slot_of_group = []
            for s in Slot.objects.filter(
                    groupid=Group.objects.get(name=gp.name).pk).all():
                slot_counter += 1
                Registered_slot_of_group.append(
                    {'id': s.slotid, 'start': s.starttime, 'end': s.endtime})
            suggested_number = int(number_Of_Group_Member * 1.25)
            if suggested_number < 25:
                suggested_number = 25
            if slot_counter < suggested_number:
                RegisteredSlotsReturn.append({
                    'group': gp.name,
                    'member_count': number_Of_Group_Member,
                    'slots': Registered_slot_of_group,
                    'suggested': suggested_number,
                    'current': slot_counter,
                    'slot_enough': False})
            else:
                RegisteredSlotsReturn.append({
                    'group': gp.name,
                    'member_count': number_Of_Group_Member,
                    'slots': Registered_slot_of_group,
                    'suggested': suggested_number,
                    'current': slot_counter,
                    'slot_enough': True})

    # form handling
    if request.method == 'POST':
        form = forms.NameForm(request.POST)
        context['form'] = forms
        if form.is_valid():
            # debug information
            if DEBUG:
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

            already_registered_slots = Slot.objects.filter(
                groupid=Group.objects.get(name=form.cleaned_data['group']).pk)
            period_end = period_start
            for _i in range(0, numberOfMeet):
                session_start = period_end
                period_end = period_end + \
                    datetime.timedelta(minutes=meetingLen)
                for s in already_registered_slots:
                    if (
                        (pytz.UTC.localize(session_start) >= s.starttime and pytz.UTC.localize(session_start) <= s.endtime) or
                        (pytz.UTC.localize(period_end) >= s.starttime and pytz.UTC.localize(period_end) <= s.endtime) or
                        (pytz.UTC.localize(session_start) >= s.starttime and pytz.UTC.localize(period_end) <= s.endtime) or
                        (pytz.UTC.localize(session_start) <= s.starttime and pytz.UTC.localize(
                            period_end) >= s.endtime)
                    ):
                        timecollision = True
                        formError = "ERROR: At least one of the timeslot collided, please double check or remove existing slot(s)"
                meetingSession.append(
                    {'startTime': session_start, 'endTime': (period_end + datetime.timedelta(minutes=-1))})

            if DEBUG:
                print(period_start)
                print(period_end)
                for x in meetingSession:
                    print(
                        " start:", x['startTime'], "end:", x['endTime'])

            # prepare the checking
            if not timecollision:
                computed_detail = {
                    'not_empty': True,
                    'group': form.cleaned_data['group'],
                    'startTime_str': period_start_str,
                    'startTime': period_start,
                    'endTime': period_end,
                    'duration': meetingLen,
                    'no_of_meeting': numberOfMeet}
        else:
            computed_detail = {'not_empty': False}

    return render(request, 'calendar.html', {
        'base_return': base_return,
        'formError': formError,
        'confirmForm': forms.ConfirmForm,
        'group_list': grouplist,
        'availableTimes': RegisteredSlotsReturn,
        'computed_details': computed_detail
    })

def confirm(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            allowed_group = Timetable.objects.get().phase1_group_name
            form = forms.ConfirmForm(request.POST)
            user_allowed_to_access = False
            user_in_target_group = False

            if DEBUG:
                print(form)

            if form.is_valid():
                userid = User.objects.get(username=request.user).pk
                group = User.objects.get(username=request.user).groups

                for gp in request.user.groups.all():
                    if gp.name == allowed_group:
                        user_allowed_to_access = True
                    if gp.name == form.cleaned_data['confirm_group']:
                        user_in_target_group = True

                if user_allowed_to_access and user_in_target_group:
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
                            endtime=period_end +
                            datetime.timedelta(minutes=-1),
                            groupid=Group.objects.get(name=group).pk,
                            active=True
                        )

                    return HttpResponseRedirect('/calendar/')
                return HttpResponse(
                    '<h1>Unauthorised Access</h1>', status=403)
            return HttpResponse('<h1>Invalid Form</h1>', status=404)
        return HttpResponse('<h1>ACCEESS DENIED</h1>', status=404)
    return HttpResponse(
        '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)


def remove(request):
    if request.user.is_authenticated:
        userid = User.objects.get(username=request.user).pk
        group = User.objects.get(username=request.user).groups

        # variable for generating slot list
        RegisteredSlotsReturn = []
        grouplist = ['All']
        cur_group = 'All'

        formError = ''
        formSuccess = ''

        user_already_selected = {'flag': False}
        failedSubmission = {'flag': False}

        if 'cur_group' in request.session:
            cur_group = request.session['cur_group']

        access_check = check_user_allowed_to_access_phase1(request.user)
        if access_check['flag']:
            grouplist = grouplist + access_check['grouplist']
            if request.method == "POST":
                print("POST:", request.POST)
                if 'group_select' in request.POST:
                    form = forms.RemoveGroupSelectForm(request.POST)
                    if form.is_valid():
                        print("GP select valid")
                        cur_group = form.cleaned_data['groupselect']
                        request.session['cur_group'] = form.cleaned_data['groupselect']

                if 'slot_select' in request.POST:
                    form = forms.RemoveSlotSelectForm(request.POST)
                    if form.is_valid():
                        valid = True

                        # split the form into list
                        SelectList_reurn = form.cleaned_data['selectionlist']
                        slotSelectList = list(SelectList_reurn.split(","))

                        # check is all inputed value is integer
                        for t in slotSelectList:
                            if valid:
                                try:
                                    int(t)
                                except BaseException:
                                    formError = "Error: One of the selected item cannot be recognised"
                                    valid = False

                        # check if ther is duplicated slot
                        if valid:
                            for i in range(0, len(slotSelectList)):
                                for x in range(i + 1, len(slotSelectList)):
                                    if int(slotSelectList[i]) == int(
                                            slotSelectList[x]):
                                        valid = False
                                        formError = "Error: One item is repeated"

                        # check if all slot are allowed for this group
                        if valid:
                            allowed_slotID_for_this_group = Slot.objects.filter(
                                groupid=Group.objects.get(name=form.cleaned_data['group']).pk).all()
                            for i in slotSelectList:
                                slotID_exist_in_this_group = False
                                for s in allowed_slotID_for_this_group:
                                    if int(i) == s.slotid:
                                        slotID_exist_in_this_group = True
                                if not slotID_exist_in_this_group:
                                    valid = False
                                    formError = "ERROR: At lease one of the slotID is invalid"

                        # store it in DB if all check passed
                        if valid:
                            groupid = Group.objects.get(
                                name=form.cleaned_data['group']).pk
                            for i in range(0, len(slotSelectList)):
                                Slot.objects.filter(
                                    groupid=groupid, slotid=slotSelectList[i]).all().delete()
                            formSuccess = "SUCCESS: your available slots is updated"
                        else:
                            failedSubmission['flag'] = True
                            failedSubmission['list'] = SelectList_reurn

                        if DEBUG:
                            print("Selection Form Valid")
                            print('slotSelectList: ', slotSelectList)

            # generate the timetable list
            if cur_group == 'All':
                for gp in request.user.groups.all():
                    if Slot.objects.filter(groupid=Group.objects.get(
                            name=gp.name).pk).count() > 0:
                        Registered_slot_of_group = []
                        for s in Slot.objects.filter(
                                groupid=Group.objects.get(name=gp.name).pk).all():
                            Registered_slot_of_group.append(
                                {'id': s.slotid, 'start': s.starttime, 'end': s.endtime})
                        RegisteredSlotsReturn.append(
                            {'group': gp.name, 'slots': Registered_slot_of_group})
                if DEBUG:
                    print("RegisteredSlotsReturn: ", RegisteredSlotsReturn)
            else:
                Registered_slot_of_group = []
                groupid = Group.objects.get(name=cur_group).pk
                for s in Slot.objects.filter(groupid=groupid).all():
                    Registered_slot_of_group.append(
                        {'id': s.slotid, 'start': s.starttime, 'end': s.endtime})
                # Read previous record of user submitted choice of that group
                RegisteredSlotsReturn.append(
                    {'group': cur_group, 'slots': Registered_slot_of_group})

            return render(request, 'calendar/remove.html', {
                'formError': formError,
                'formSuccess': formSuccess,
                'currentGroup': cur_group,
                'grouplist': grouplist,
                'availableTimes': RegisteredSlotsReturn,
                'previousSelection': user_already_selected,
                'failedSubmission': failedSubmission
            })
        return HttpResponse('<h1>ACCEESS DENIED</h1>', status=404)
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
        if access_check['flag']:
            grouplist = access_check['grouplist']
            if request.method == 'POST':
                form = forms.ChangeMinRequired(request.POST)
                if form.is_valid():
                    if form.cleaned_data['minrequiredslot'] <= Slot.objects.filter(
                            groupid=Group.objects.get(name=form.cleaned_data['groupname']).pk).count():
                        Groupdetail.objects.filter(
                            groupid=Group.objects.get(
                                name=form.cleaned_data['groupname']).pk).update(
                            min_required_slot=form.cleaned_data['minrequiredslot'])
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
                    gpDetail = Groupdetail.objects.filter(
                        groupid=groupID).get()
                    miniumSlotReturn.append(
                        {'groupname': gp, 'minslot': gpDetail.min_required_slot})

            return render(request, 'calendar/setmin.html', {
                'formError': formError,
                'formSuccess': formSuccess,
                'miniumSlotReturn': miniumSlotReturn
            })
        return HttpResponse('<h1>ACCEESS DENIED</h1>', status=404)
    return HttpResponse(
        '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)


def check_user_allowed_to_access_phase1(user):
    user_allowed_to_access = False
    allowed_group = Timetable.objects.get().phase1_group_name
    phase = -1
    grouplist = []
    if DEBUG:
        phase = 1

    for gp in user.groups.all():
        grouplist.append(gp.name)
        if gp.name == allowed_group:
            user_allowed_to_access = True

    if phase == 1 and user_allowed_to_access:
        return {'flag': True, 'grouplist': grouplist}
    return {'flag': False, 'grouplist': grouplist}


def getGroupMemberCount(groupname):
    counter = 0
    all_users = User.objects.all()
    for u in all_users:
        usergroup = u.groups.all()
        for gp in usergroup:
            if gp.name == groupname:
                counter += 1
    return counter
