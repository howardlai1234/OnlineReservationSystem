from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'message.html', {
            'username':request.session['username'],

            })



def create_new(request):
    return HttpResponse("ORS-New_Message <br> Work in Progress")
