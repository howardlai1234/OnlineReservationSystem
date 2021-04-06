from munkres import Munkres
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
# Create your views here.

def home(request):
   return HttpResponse("Hello")