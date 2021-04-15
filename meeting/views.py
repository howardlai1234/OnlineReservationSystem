from datetime import date
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.contrib.auth.models import User
from dashboard.models import Meeting
from meeting import forms
from message.views import sent_new_message
from ORS.function import base_data
from ORS.settings import DEBUG
# Create your views here.

# HTML views


def home(request):
    if not request.user.is_authenticated:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)

    base_return = base_data(request.user)
    userid = User.objects.get(username=request.user).pk

    today_meeting = []
    today_meeting_count = Meeting.objects.filter(
        hostid=userid, date=date.today()).count()
    today_meeting_count += Meeting.objects.filter(
        participantid=userid, date=date.today()).count()
    future_meeting = []
    future_meeting_count = Meeting.objects.filter(
        hostid=userid, date__gt=date.today()).count()
    future_meeting_count += Meeting.objects.filter(
        participantid=userid, date__gt=date.today()).count()
    pass_meeting = []
    pass_meeting_count = Meeting.objects.filter(
        hostid=userid, date__lt=date.today()).count()
    pass_meeting_count += Meeting.objects.filter(
        participantid=userid, date__lt=date.today()).count()

    if today_meeting_count > 0:
        today_meeting = meeting_list(userid, 0)
    if future_meeting_count > 0:
        future_meeting = meeting_list(userid, 1)
    if pass_meeting_count > 0:
        pass_meeting = meeting_list(userid, -1)

    return render(request, "meeting.html", {
        'base_return': base_return,
        'today_meeting': today_meeting,
        'today_meeting_count': today_meeting_count,
        'future_meeting': future_meeting,
        'future_meeting_count': future_meeting_count,
        'pass_meeting': pass_meeting,
        'pass_meeting_count': pass_meeting_count,
    })


def view(request):
    if not request.user.is_authenticated:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)

    base_return = base_data(request.user)
    userID = User.objects.get(username=request.user).pk
    meetingID = request.GET.get('id', '')
    if not check_user_can_view(userID, meetingID):
        return HttpResponseNotFound(
            '<h1>404 ERROR: message not found</h1>', status=404)
    try:
        meeting = Meeting.objects.filter(meetingid=meetingID).get()
        host = User.objects.get(pk=meeting.hostid).username
        participant = User.objects.get(pk=meeting.participantid).username
    except Meeting.DoesNotExist:
        raise HttpResponseNotFound(
            '<h1>404 ERROR: message not found</h1>', status=404)

    return render(request, "meeting/view.html", {
        'base_return': base_return,
        'meeting': meeting,
        'host': host,
        'participant': participant
    })

    return HttpResponse("ORS-Meeting <br> Work in Progress")


def manage(request):
    if not request.user.is_authenticated:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)

    base_return = base_data(request.user)
    userID = User.objects.get(username=request.user).pk
    meetingID = request.GET.get('id', '')
    if not check_user_can_manage(userID, meetingID):
        return HttpRsponseNotFound(
            '<h1>403 ERROR: ACCESS DENIED</h1>', status=403)
    try:
        meeting = Meeting.objects.filter(meetingid=meetingID).get()
        host = User.objects.get(pk=meeting.hostid).username
        participant = User.objects.get(pk=meeting.participantid).username
    except Meeting.DoesNotExist:
        raise HttpResponseNotFound(
            '<h1>404 ERROR: message not found</h1>', status=404)
    formError = ""
    formSuccess = ""
    if request.method == 'POST':
        form = forms.ManageForm(request.POST)
        if form.is_valid():
            if DEBUG:
                print("form_valid")
            # starttime = form.cleaned_data['starttime']
            # endtime = form.cleaned_data['endtime']
            if form.cleaned_data['starttime'] >= form.cleaned_data['endtime']:
                formError = "ERROR: endtime cannot be equal or eariler then start time"
            else:
                Meeting.objects.filter(pk=int(form.cleaned_data['meetingid'])).update(
                    date=form.cleaned_data['date'],
                    starttime=form.cleaned_data['starttime'],
                    endtime=form.cleaned_data['endtime'],
                    name=form.cleaned_data['name'],
                    remark=form.cleaned_data['remark']
                )
                formSuccess = "SUCCESS: The meeting details has been updated"
    return render(request, "meeting/manage.html", {
        'base_return': base_return,
        'date_str': meeting.date.strftime("%Y-%m-%d"),
        'starttime_str': meeting.starttime.strftime("%H:%M"),
        'endtime_str': meeting.endtime.strftime("%H:%M"),
        'meeting': meeting,
        'host': host,
        'participant': participant,
        'formSuccess': formSuccess,
        'formError': formError
    })


def create(request):
    if not request.user.is_authenticated:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)

    if not request.user.is_staff:
        return HttpResponse('<h1>ACCEESS DENIED</h1>', status=403)
    base_return = base_data(request.user)
    name = ''
    participant = ''
    remark = 'N/A'
    date_str = ''
    starttime_str = ''
    endtime_str = ''
    form_return = {}

    formError = ""
    formSuccess = ""
    participantID = 0

    error = False
    valid = False
    if request.method == 'POST':
        form = forms.CreateForm(request.POST)
        if form.is_valid():
            valid = True
            if DEBUG:
                print("form valid")
            name = form.cleaned_data['name']
            date = form.cleaned_data['date']
            starttime = form.cleaned_data['starttime']
            endtime = form.cleaned_data['endtime']
            host = form.cleaned_data['host']
            participant = form.cleaned_data['participant']
            remark = form.cleaned_data['remark']
            date_str = date.strftime("%Y-%m-%d")
            starttime_str = starttime.strftime("%H:%M")
            endtime_str = endtime.strftime("%H:%M")

            form_return['name'] = name
            form_return['date_str'] = date_str
            form_return['starttime_str'] = starttime_str
            form_return['endtime_str'] = endtime_str
            form_return['host'] = host
            form_return['participant'] = participant
            form_return['remark'] = remark

            if valid and date <= date.today():
                valid = False
                error = True
                formError = "ERROR: You can not a meeting that scheduled on today or before"

            if valid and starttime >= endtime:
                valid = False
                error = True
                formError = "ERROR: endtime cannot be equal or eariler then start time"

            if valid and User.objects.filter(username=host).count() != 1:
                valid = False
                error = True
                formError = "Error: Host Username not found"

            if valid and User.objects.filter(
                    username=participant).count() != 1:
                valid = False
                error = True
                formError = "Error: Participant Username not found"

            if valid:
                hostID = User.objects.get(username=host).pk
                participantID = User.objects.get(username=participant).pk
                Meeting.objects.create(
                    hostid=hostID,
                    participantid=participantID,
                    date=date,
                    starttime=starttime,
                    endtime=endtime,
                    name=name,
                    remark=remark,
                    statusid=1
                )
                meeting_id = Meeting.objects.get(
                    hostid=hostID,
                    participantid=participantID,
                    date=date,
                    starttime=starttime,
                    endtime=endtime,
                    name=name,
                    remark=remark,
                    statusid=1
                ).pk
                sent_new_message(
                    0,
                    hostID,
                    0,
                    meeting_id,
                    "A new meeting is generated",
                    "A new meeting is generated by " +
                    str(request.user) + ", between " + host + " and " +
                    participant + ". please check it in meeting page for details"
                )
                sent_new_message(
                    0,
                    participantID,
                    0,
                    meeting_id,
                    "A new meeting is generated",
                    "A new meeting is generated by " +
                    str(request.user) + ", between " + host + " and " +
                    participant + ". please check it in meeting page for details"
                )
                formSuccess = "SUCCESS: A new meeting is created, An automatic message is sent to host and participant"

    return render(request, "meeting/create.html", {
        'base_return': base_return,
        'form_return': form_return,
        'error': error,
        'formSuccess': formSuccess,
        'formError': formError
    })

# Internal Functions


def check_user_can_view(userID, meetingID):
    if Meeting.objects.filter(hostid=userID, meetingid=meetingID).count(
    ) == 1 or Meeting.objects.filter(participantid=userID, meetingid=meetingID).count() == 1:
        return True
    return False


def check_user_can_manage(userID, meetingID):
    if Meeting.objects.filter(hostid=userID, meetingid=meetingID).count() == 1:
        return True
    return False


def meeting_list(userID, date_prem):
    return_list = []
    date_prem_valid = False
    if date_prem == 0:
        meeting = Meeting.objects.filter((Q(hostid=userID) | Q(
            participantid=userID)) & Q(date=date.today())).all()
        date_prem_valid = True
    if date_prem == 1:
        meeting = Meeting.objects.filter((Q(hostid=userID) | Q(
            participantid=userID)) & Q(date__gt=date.today())).all()
        date_prem_valid = True
    if date_prem == -1:
        meeting = Meeting.objects.filter((Q(hostid=userID) | Q(
            participantid=userID)) & Q(date__lt=date.today())).all()
        date_prem_valid = True
    if date_prem_valid:
        for m in meeting:
            is_host = False
            if userID == m.hostid:
                is_host = True
            return_list.append({
                'meetingid': m.meetingid,
                'hostname': User.objects.get(pk=m.hostid).username,
                'participantname': User.objects.get(pk=m.participantid).username,
                'date': m.date,
                'starttime': m.starttime,
                'endtime': m.endtime,
                'name': m.name,
                'ishost': is_host
            })
    return return_list
