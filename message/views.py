from django.shortcuts import render
from django.http import HttpResponse
from django.db import connections
from django.db.utils import OperationalError
from django.contrib.auth.models import User
from dashboard.models import Message
from ORS.settings import DEBUG

# Create your views here.


def home(request):

    if request.user.is_authenticated:
        userid = User.objects.get(username=request.user).pk
        
        received_message_return = []
        received_message_count = Message.objects.filter(receiverid=userid).count()

        sent_message_return = []
        sent_message_count = Message.objects.filter(senderid=userid).count()        

        if received_message_count > 0:
            received_message = Message.objects.filter(receiverid=userid).all()
            # for message in received_message:
            #     print()
            print("Title:", received_message[0].title)
            for message in received_message:
                print("message title:", message.title)
                print("sender:",User.objects.get(pk=int(message.senderid)))
                print(message.body)
                received_message_return.append({
                    'messageid':message.messageid,
                    'title': message.title, 
                    'sender': User.objects.get(pk=int(message.senderid)), 
                    'body': message.body
                })
                if message.viewed==0:
                    Message.objects.filter(messageid=message.messageid).update(viewed=1)

        if sent_message_count > 0:
            sent_message = Message.objects.filter(senderid=userid).all()
            for message in sent_message:
                print("message title:", message.title)
                print("sender:",User.objects.get(pk=int(message.senderid)))
                print(message.body)
                if message.viewed==0:
                    sent_message_return.append({
                        'messageid':message.messageid,
                        'title': message.title, 
                        'sender': User.objects.get(pk=int(message.receiverid)), 
                        'body': message.body, 
                        'viewed': "No"
                 })
                else:
                    sent_message_return.append({
                        'messageid':message.messageid, 
                        'title': message.title, 
                        'sender': User.objects.get(pk=int(message.receiverid)), 
                        'body': message.body, 
                        'viewed': "Yes"
                    })

        return render(request, "message.html", {
            'received_message_count': received_message_count,
            'received_message': received_message_return,
            'sent_message_count': sent_message_count,
            'sent_message': sent_message_return
        })
    ##the following code is for older version which uses RAW SQL

    # if 'userid' in request.session:
    #     userid = request.session['userid']
    #     db_conn = connections['default']
    #     cursor = db_conn.cursor()
    #     sql = 'SELECT messageID, sendTime, title, body FROM message WHERE receiverID="' + \
    #         str(userid) + '" ORDER BY messageID'
    #     cursor.execute(sql)
    #     row = cursor.fetchall()

    #     return render(request, 'message.html', {
    #         'username': request.session['username'],

    #     })
    else:
        return HttpResponse('<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>')


def view(request):
    if request.user.is_authenticated:
        print( "Nothing to see here, move along")
        messageID = request.GET.get('id','')
        userid = User.objects.get(username=request.user).pk
        if Message.objects.filter(receiverid=userid, messageid=messageID).count() == 1 or Message.objects.filter(senderid=userid, messageid=messageID).count() == 1:
            message = Message.objects.filter(messageid=messageID).get()
            #message_return = {}
            return render(request, "message/message_view.html", {'message': message})

    ##the following code is for older version which uses RAW SQL
    # if 'userid' in request.session:
    #     if request.GET != '':
    #         print("get:", request.GET)
    #         return HttpResponse('ok')
    #     else:
    #         return HttpResponse('<h1>ACCEESS DENIED</h1> <br> Incorrect or messing messageID <br> <br><a href="/message">Back</a>')
        return HttpResponse( messageID , "Nothing to see here, move along")
    else:
        return HttpResponse('<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>')


def create_new(request):
    return HttpResponse("ORS-New_Message <br> Work in Progress")
