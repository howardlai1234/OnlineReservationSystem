from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    if 'userid' in request.session:
        db_conn = connections['default']
        cursor = db_conn.cursor()
        sql ='SELECT messageID, sendTime, title, bodyw FROM message WHERE receiverID="' + str(userid) + '" ORDER BY messageID'
        cursor.execute(sql)
        row = cursor.fetchall()

        return render(request, 'message.html', {
                'username':request.session['username'],

                })
    else:
        return HttpResponse('<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>')



def create_new(request):
    return HttpResponse("ORS-New_Message <br> Work in Progress")
