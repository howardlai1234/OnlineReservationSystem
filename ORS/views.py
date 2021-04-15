from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard/')
    return HttpResponseRedirect('/accounts/login/')
