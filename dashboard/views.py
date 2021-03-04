from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    username=""
    meeting_counter = message_counter = 0
    if 'username' in request.session:
        username = request.session['username']
        userid = request.session['userid']
        return render(request, 'dashboard.html', {
            'username': username,
            'userid':userid,
            'meeting_counter': meeting_counter,
            'message_counter': message_counter
    })
    else:
        return HttpResponse('<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>')
