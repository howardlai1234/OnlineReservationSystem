from datetime import date
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.contrib.auth.models import User
from dashboard.models import Meeting

# Create your views here.


def home(request):
    if not request.user.is_authenticated:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)

    userid = User.objects.get(username=request.user).pk

    today_meeting = []
    today_meeting_count = Meeting.objects.filter(hostid=userid, date=date.today()).count()
    today_meeting_count += Meeting.objects.filter(participantid=userid, date=date.today()).count()
    future_meeting = []
    future_meeting_count = Meeting.objects.filter(hostid=userid, date__gt=date.today()).count()
    future_meeting_count += Meeting.objects.filter(participantid=userid, date__gt=date.today()).count()
    pass_meeting = []
    pass_meeting_count = Meeting.objects.filter(hostid=userid, date__lt=date.today()).count()
    pass_meeting_count += Meeting.objects.filter(participantid=userid, date__lt=date.today()).count()

    if today_meeting_count > 0:
        today_meeting = meeting_list(userid, 0)
    if future_meeting_count > 0:
        future_meeting = meeting_list(userid, 1)
    if pass_meeting_count > 0:
        pass_meeting = meeting_list(userid, -1)


    return render(request, "meeting.html", {
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
    return render(request, "meeting/view.html",{
        'meeting': meeting,
        'host': host,
        'participant': participant
    })

    return HttpResponse("ORS-Meeting <br> Work in Progress")

def manage(request):
    if not request.user.is_authenticated:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)

    userID = User.objects.get(username=request.user).pk
    meetingID = request.GET.get('id', '')  
    if not check_user_can_manage(user, meetingID):
        return HttpRsponseNotFound('<h1>403 ERROR: ACCESS DENIED</h1>', status=403)

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
        meeting = Meeting.objects.filter((Q(hostid=userID) | Q(participantid=userID)) & Q(date=date.today())).all()
        date_prem_valid = True
    if date_prem == 1:
        meeting = Meeting.objects.filter((Q(hostid=userID) | Q(participantid=userID)) & Q(date__gt=date.today())).all()
        date_prem_valid = True
    if date_prem == -1:
        meeting = Meeting.objects.filter((Q(hostid=userID) | Q(participantid=userID)) & Q(date__lt=date.today())).all()
        date_prem_valid = True
    if date_prem_valid:
        for m in meeting:
            return_list.append({
                'meetingid': m.meetingid,
                'hostname': User.objects.get(pk=m.hostid).username,
                'participantname': User.objects.get(pk=m.participantid).username,
                'date': m.date,
                'starttime': m.starttime,
                'endtime': m.endtime,
                'name': m.name
            })
            print("return_list--", return_list)
    return return_list