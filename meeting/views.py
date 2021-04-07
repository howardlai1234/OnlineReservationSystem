from datetime import date
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
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
        today_meeting = (userid, 'date')
    if future_meeting_count > 0:
        today_meeting = (userid, 'date__gt')
    if pass_meeting_count > 0:
        today_meeting = (userid, 'date__lt')

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
    if not check_user_can_view(UserID, meetingID):
        return HttpResponseNotFound(
            '<h1>404 ERROR: message not found</h1>', status=404)
    try:
        meeting = Meeting.objects.filter(meetingid=meetingID).get()
        host = User.objects.get(pk=meeting.hostid).username
        participant = User.objects.get(pk=meeting.participantid).username
    except Meeting.DoesNotExist:
        raise HttpResponseNotFound(
            '<h1>404 ERROR: message not found</h1>', status=404)
    

        
    
    return HttpResponse("ORS-Meeting <br> Work in Progress")

def manage(request):
    if not request.user.is_authenticated:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)

    userID = User.objects.get(username=request.user).pk
    meetingID = request.GET.get('id', '')  
    if not check_user_can_manage(user, meetingID):
        return HttpResponseNotFound('<h1>403 ERROR: ACCESS DENIED</h1>', status=403)
    



def check_user_can_view(userID, meetingID):
    if Meeting.objects.filter(hostid=userid, meetingid=meetingID).count(
        ) == 1 or Meeting.objects.filter(participantid=userid, meetingid=meetingID).count() == 1:
        return True
    return False

def check_user_can_manage(userID, meetingID):
    if Meeting.objects.filter(hostid=userid, meetingid=meetingID).count() == 1:
        return True
    return False

def meeting_list(UserID, date_prem):
    return_list = []
    meeting = Message.objects.filter((Q(hostid=userid) | Q(participantid=userid)) & Q(date_prem=date.today())).all()
    for m in meeting:
        return_list.append({
            'meetingid': m.meetingid,
            'hostid': User.objects.get(pk=m.hostid).username,
            'participantid': User.objects.get(pk=m.participantid).username,
            'date': m.date,
            'starttime': m.starttime,
            'endtime': m.endtime,
            'name': m.name
        })
    return return_list