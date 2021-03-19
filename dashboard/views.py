from django.shortcuts import render
from django.http import HttpResponse
from django.db import connections
from django.db.utils import OperationalError
from django.contrib.auth.models import User
# Create your views here.


def home(request):

    if request.user.is_authenticated:
        print(request)

        #username = request.session['username']
        #userid = request.session['userid']
        meeting_counter = message_counter = 0
        username = ""
        userid = User.objects.get(username=request.user).pk
        # setup DB connection
        #db_conn = connections['default']
        #cursor = db_conn.cursor()

        # retrive message count from DB
        #sql = 'SELECT count(messageID) FROM Message WHERE receiverID="' + \
        #    str(userid) + '"'
        #cursor.execute(sql)
        #row = cursor.fetchone()
        #message_counter = row[0]

        # retrive meeting count from DB
        #sql = 'SELECT count(meetingID) FROM Meeting WHERE hostID="' + \
        #    str(userid) + '" OR participantID="' + str(userid) + '"'
        #cursor.execute(sql)
        #row = cursor.fetchone()
        #meeting_counter = row[0]

        return render(request, 'dashboard.html', {
            'username': request.user,
            'userid': userid,
            'meeting_counter': meeting_counter,
            'message_counter': message_counter
        })
    else:
        return HttpResponse('<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>')
