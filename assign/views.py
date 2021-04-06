from munkres import Munkres, print_matrix, make_cost_matrix, DISALLOWED
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.contrib.auth.models import User, Group
from dashboard.models import Groupdetail, Meeting, Slot
from ORS.settings import DEBUG
# Create your views here.

def home(request):
   #Access control measure
   if not request.user.is_authenticated:
      return HttpResponse(
        '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)
   if not request.user.is_superuser:
      return HttpResponse('<h1>ACCEESS DENIED</h1>', status=404)
   # D = DISALLOWED
   # matrix = [[6, 4, 2, 25, 20, D, D, D],
   #           [2, 20, D, D, 3, 25, 6, D],
   #           [4, 2, 6, 25, D, D, D, 20],
   #           [4, 6, 2, 25, 20, D, D, D],
   #           [4, D, 6, D, 2, 20, 25, D],
   #           [4, 2, 6, D, D, 25, 20, D]
   #           ]
   # m = Munkres()
   # indexes = m.compute(matrix)
   # print_matrix(matrix, msg='Lowest cost through this matrix:')
   # total = 0
   # for row, column in indexes:
   #    value = matrix[row][column]
   #    total += value
   #    print(f'({row}, {column}) -> {value}')
   # print(f'total cost: {total}')



   return HttpResponse("Hello")