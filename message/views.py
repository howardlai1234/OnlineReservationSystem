from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.db import connections
from django.db.utils import OperationalError
from django.contrib.auth.models import User
from dashboard.models import Message
from ORS.function import base_data
from ORS.settings import DEBUG
from message import forms

# Create your views here.


def home(request):

    if request.user.is_authenticated:
        base_return = base_data(request.user)  
        userid = User.objects.get(username=request.user).pk

        received_message_return = []
        received_message_count = Message.objects.filter(
            receiverid=userid).count()

        sent_message_return = []
        sent_message_count = Message.objects.filter(senderid=userid).count()

        if received_message_count > 0:
            received_message = Message.objects.filter(receiverid=userid).all()
            # for message in received_message:
            #     print()
            print("Title:", received_message[0].title)
            for message in received_message:
                if int(message.senderid) == 0:
                    sender = 'SYSTEM'
                else:
                    sender = User.objects.get(pk=int(message.senderid))
                if DEBUG:
                    print("message title:", message.title)
                    print("sender:", sender)
                    print(message.body)
                received_message_return.append({
                    'messageid': message.messageid,
                    'title': message.title,
                    'sender': sender,
                    'body': message.body
                })
                if message.viewed == 0:
                    Message.objects.filter(
                        messageid=message.messageid).update(
                        viewed=1)

        if sent_message_count > 0:
            sent_message = Message.objects.filter(senderid=userid).all()
            for message in sent_message:
                if DEBUG:
                    print("message title:", message.title)
                    print(
                        "sender:", User.objects.get(
                            pk=int(
                                message.senderid)))
                    print(message.body)
                if message.viewed == 0:
                    sent_message_return.append({
                        'messageid': message.messageid,
                        'title': message.title,
                        'sender': User.objects.get(pk=int(message.receiverid)),
                        'body': message.body,
                        'viewed': "No"
                    })
                else:
                    sent_message_return.append({
                        'messageid': message.messageid,
                        'title': message.title,
                        'sender': User.objects.get(pk=int(message.receiverid)),
                        'body': message.body,
                        'viewed': "Yes"
                    })

        return render(request, "message.html", {
            'base_return': base_return,
            'received_message_count': received_message_count,
            'received_message': received_message_return,
            'sent_message_count': sent_message_count,
            'sent_message': sent_message_return
        })
    # the following code is for older version which uses RAW SQL

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
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)


def view(request):
    if request.user.is_authenticated:
        base_return = base_data(request.user)  
        messageID = request.GET.get('id', '')
        userid = User.objects.get(username=request.user).pk
        if Message.objects.filter(receiverid=userid, messageid=messageID).count(
        ) == 1 or Message.objects.filter(senderid=userid, messageid=messageID).count() == 1:
            try:
                message = Message.objects.filter(messageid=messageID).get()
                receiver = User.objects.get(pk=message.receiverid).username
            except Message.DoesNotExist:
                raise HttpResponseNotFound(
                    '<h1>404 ERROR: message not found</h1>')
            if message.senderid == 0:
                sender = "SYSTEM"
            else:
                try:
                    sender = User.objects.get(pk=message.senderid).username 
                except Message.DoesNotExist:
                    raise HttpResponseNotFound(
                        '<h1>404 ERROR: message not found</h1>')
            message_return = {}
            return render(request, "message/view.html", {
                'base_return': base_return,
                'message': message,
                'sender': sender,
                'receiver': receiver
            })

    # the following code is for older version which uses RAW SQL
    # if 'userid' in request.session:
    #     if request.GET != '':
    #         print("get:", request.GET)
    #         return HttpResponse('ok')
    #     else:
    # return HttpResponse('<h1>ACCEESS DENIED</h1> <br> Incorrect or messing
    # messageID <br> <br><a href="/message">Back</a>')
        return HttpResponseNotFound('<h1>404 ERROR: message not found</h1>', status=404)
    return HttpResponse(
        '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)


def create_new(request):
    base_return = base_data(request.user)  
    formError = ""
    formSuccess = ""
    message_is_valid = -1
    receiverID = 0

    if request.user.is_authenticated:
        userid = User.objects.get(username=request.user).pk
        if request.method == 'POST':
            form = forms.NameForm(request.POST)
            if form.is_valid():
                if DEBUG == True:
                    print("Form Valid")
                    print("receiver: ", form.cleaned_data['receiver'])
                    print("title: ", form.cleaned_data['title'])
                    print("Message body: ", form.cleaned_data['body'])
                    print("current time: ", datetime.now())
                if User.objects.filter(
                        username=form.cleaned_data['receiver']).count() == 1:
                    receiverID = User.objects.get(
                        username=form.cleaned_data['receiver']).pk
                    if receiverID == userid:
                        message_is_valid = 0
                        formError = formError + "ERROR: You cannot sent message to yourself"
                    else:
                        #####################################
                        ## Moved to a independent function ##
                        #####################################
                        # Message.objects.create(
                        #     senderid=userid,
                        #     receiverid=receiverID,
                        #     sendtime=datetime.now(),
                        #     viewed=0,
                        #     title=form.cleaned_data['title'],
                        #     body=form.cleaned_data['body']
                        # )
                        message_is_valid = sent_new_message(
                            userid, receiverID, 0, 0, form.cleaned_data['title'], form.cleaned_data['body'])
                        formSuccess = "Message sent Successfully"
                else:
                    message_is_valid = 0
                    formError = "ERROR: Receiver Not found"

            else:
                if DEBUG == True:
                    print("Form Invalid")
                formError = "ERROR: Invalid Mesage, please check if the either title or main body exceed character limit and retry later."
                formError = formError + "<br> if the problem contitue, pls contact an administrator"
        return render(request, "message/create.html", {
            'base_return': base_return,
            'formSuccess': formSuccess,
            'formError': formError,

        })
    else:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)

def sent_new_message(senderID, receiverID, referenceID,
                     meetingID, title, body):
    Message.objects.create(
        senderid=senderID,
        receiverid=receiverID,
        referenceid=referenceID,
        meetingid=meetingID,
        sendtime=datetime.now(),
        viewed=0,
        title=title,
        body=body
    )
