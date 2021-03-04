from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("ORS-Message <br> Work in Progress")


def create_new(request):
    return HttpResponse("ORS-New_Message <br> Work in Progress")
