from munkres import Munkres, print_matrix, make_cost_matrix, DISALLOWED
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.contrib.auth.models import User, Group
from dashboard.models import Groupdetail, Meeting, Slot
from slotSelect.models import Selection
from ORS.settings import DEBUG
# Create your views here.

def home(request):
   #Access control measure
   if not request.user.is_authenticated:
      return HttpResponse(
        '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)
   if not request.user.is_superuser:
      return HttpResponse('<h1>ACCEESS DENIED</h1>', status=404)
   for gp in Group.objects.all():
      
      groupID = Group.objects.get(name=gp.name).pk
      if DEBUG:
         print ('Group Name:', gp.name, 'Group id:', groupID)
      selection = Selection.objects.filter(groupid=groupID).order_by('userid', 'slotid')
      if DEBUG:
         for s in selection:
            print("slot detail:", s.groupid, s.userid, s.slotid, s.userorder)
      
   for usr in User.objects.all():
      print ("username:", usr.username, "id:", User.objects.get(username=usr.username).pk)
   D = DISALLOWED
   matrix = [[6, 4, 2, 25, 20, D, D, D],
             [2, 20, D, D, 3, 25, 6, D],
             [4, 2, 6, 25, D, D, D, 20],
             [4, 6, 2, 25, 20, D, D, D],
             [4, D, 6, D, 2, 20, 25, D],
             [4, 2, 6, D, D, 25, 20, D]
             ]
   m = Munkres()
   indexes = m.compute(matrix)
   print_matrix(matrix, msg='Lowest cost through this matrix:')
   total = 0
   print('index:', indexes)
   for row, column in indexes:
      value = matrix[row][column]
      total += value
      print(f'({row}, {column}) -> {value}')
   print(f'total cost: {total}')


   return HttpResponse("Hello")