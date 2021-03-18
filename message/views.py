from django.shortcuts import render
from django.http import HttpResponse
from django.db import connections
from django.db.utils import OperationalError

# Create your views here.


def home(request):
    if 'userid' in request.session:
        userid = request.session['userid']
        db_conn = connections['default']
        cursor = db_conn.cursor()
        sql = 'SELECT messageID, sendTime, title, body FROM message WHERE receiverID="' + \
            str(userid) + '" ORDER BY messageID'
        cursor.execute(sql)
        row = cursor.fetchall()

        return render(request, 'message.html', {
            'username': request.session['username'],

        })
    else:
        return HttpResponse('<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>')


def view(request):
    if 'userid' in request.session:
        if request.GET != '':
            print("get:", request.GET)
            return HttpResponse('ok')
        else:
            return HttpResponse('<h1>ACCEESS DENIED</h1> <br> Incorrect or messing messageID <br> <br><a href="/message">Back</a>')
    else:
        return HttpResponse('<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>')


def create_new(request):
    return HttpResponse("ORS-New_Message <br> Work in Progress")
