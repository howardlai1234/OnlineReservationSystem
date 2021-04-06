from munkres import Munkres
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
# Create your views here.

def home(request):
   if not request.user.is_authenticated:
      return HttpResponse(
        '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)
   if not request.user.is_superuser:
      return HttpResponse('<h1>ACCEESS DENIED</h1>', status=404)
   

   return HttpResponse("Hello")