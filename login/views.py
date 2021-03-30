from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from login import forms
# def home(request):
#    return HttpResponse("Hello, Django!")
from datetime import datetime
from django.views import generic
from django.db import connections
from django.db.utils import OperationalError
from django.contrib.auth import logout

from django.contrib.auth.models import User


def home(request):
    return HttpResponseRedirect('/')
    print("Hello World")
    print(User.objects.all())
    formcheck = 'null'
    sql, username, password, message = '', '', '', ''
    context = {}
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        print(request.POST)
        form = forms.NameForm(request.POST)
        context['form'] = forms
    # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            formcheck = 'success'
            print(form.cleaned_data)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Checking data from database
            db_conn = connections['default']
            cursor = db_conn.cursor()
            sql = 'SELECT count(userID) FROM User WHERE username="' + \
                form.cleaned_data['username'] + '" AND hashPW="' + \
                form.cleaned_data['password'] + '"'
            cursor.execute(sql)
            row = cursor.fetchone()
            if (row[0] == 1):
                sql = 'SELECT userID FROM User WHERE username="' + \
                    form.cleaned_data['username'] + '" AND hashPW="' + \
                    form.cleaned_data['password'] + '"'
                cursor.execute(sql)
                row = cursor.fetchone()
                request.session['userid'] = row[0]
                request.session['username'] = form.cleaned_data['username']
                return HttpResponseRedirect('/dashboard/')

        else:
            formcheck = 'not valid'
    else:
        formcheck = 'failed'
        form = forms.NameForm()

    context['form'] = form
    # print(context['form'])
    return render(request, 'login.html', {
        'current_time': str(datetime.now()),
        'username': username,
        'password': password,
        'sql': sql
    })


# Create your views here.
def pass_recov(request):
    return HttpResponse("Thank you, an administrator will contact you shortly")
    # return render(request, 'PasswordRecover.html')


# Testing

def connction_test(request):
    db_conn = connections['default']
    cursor = db_conn.cursor()
    try:
        c = db_conn.cursor()
        x = "connecting to database on LAN...<br>"
    except OperationalError:
        return HttpResponse(+ "Connection Failed")
    else:

        cursor.execute('SELECT * FROM User')
        row = cursor.fetchone()
        print(row)
        return HttpResponse(x + "Connection Successful")


def logout_service(request):
    request.session.flush()
    logout(request)
    return HttpResponseRedirect('/')


class UserListView(generic.ListView):
    model = User
