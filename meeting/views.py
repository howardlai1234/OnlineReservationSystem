from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("ORS-Meeting <br> Work in Progress")

def create_new(request):
    return HttpResponse("ORS-New_Meeting <br> Work in Progress")
