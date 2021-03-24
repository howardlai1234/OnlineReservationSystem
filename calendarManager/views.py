import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import connections
from django.db.utils import OperationalError
from ORS.settings import DEBUG
from django.contrib.auth.models import User, Group
from config.models import Currentphase, Timetable
from calendarManager import forms
#from django.contrib.auth.models import Group

# Create your views here.


def home(request):
    print("celander:", Group.objects.all())
    phase = Currentphase.objects.get().phase
    allowed_group = Timetable.objects.get().phase1_group_name
    user_allowed_to_access = 0
    grouplist = []

    timetable = []
    slotsInDB = []
    currentAvailableSlots = []
    currentAvailableSlotsReturn = ''
    previousSlotID = -1
    previousSlottDateStr = '1970-1-1'
    period_start = {}
    period_end = {}
    meetingLen = 0
    numberOfMeet = 0

    if request.user.is_authenticated:
        userid = User.objects.get(username=request.user).pk
        group = User.objects.get(username=request.user).groups
        #For Debug Function
        if DEBUG==True:
            phase = 1
            print("userid: ", userid)
        for gp in request.user.groups.all():
            grouplist.append(gp.name)
            if gp.name == allowed_group:
                user_allowed_to_access = 1
                print("Group of user: ", request.user, ":", gp.name)
        if phase == 1 and user_allowed_to_access == 1:
            context = {}
            if DEBUG == True:
                print("user allowed to access")
                print("user Group in return list:", grouplist )
  
            # form handling
            if request.method == 'POST':
                form = forms.NameForm(request.POST)
                context['form'] = forms
                if form.is_valid():
                    # debug information
                    if DEBUG == True:
                        print("Form valid")
                        print("StartHour: ", int(form.cleaned_data['startHour']))
                        print("StartMinute: ", form.cleaned_data['startMinute'])
                        print("Meeting Length: ", form.cleaned_data['meetingLength'])
                        print("Number of Meeting: ", form.cleaned_data['numberOfMeeting'])

                    # convert data from form into correct and esaily to understand variables
                    date = form.cleaned_data['date']
                    startHr = int(form.cleaned_data['startHour'])
                    startMin = int(form.cleaned_data['startMinute'])
                    meetingLen = int(form.cleaned_data['meetingLength'])
                    numberOfMeet = int(form.cleaned_data["numberOfMeeting"])
                    period_start = datetime.datetime(
                        date.year, date.month, date.day, startHr, startMin, 0)
                    meetingSession = []

                    period_end = period_start
                    for i in range(0, numberOfMeet):
                        session_start = period_end
                        period_end = period_end + \
                            datetime.timedelta(minutes=meetingLen)
                        meetingSession.append(
                            {'startTime': session_start, 'endTime': period_end})
                    #   sql =
                    print(period_start)
                    print(period_end)
                    for x in meetingSession:
                        print(" start:", x['startTime'], "end:", x['endTime'])
                # code for the old version
                # """
                # print ("date:",form.cleaned_data['date'])
                # print ("StartTime:",form.cleaned_data['startHour'], form.cleaned_data['startMinute'])
                # print ("EndTime:",form.cleaned_data['endHour'], form.cleaned_data['endMinute'])

                # #validate code here
                # start = form.cleaned_data['startHour']+form.cleaned_data['startMinute']
                # end = form.cleaned_data['endHour']+form.cleaned_data['endMinute']
                # print(start)
                # print(end)
                # if (form.cleaned_data['date']>=date.today()):
                #     if ((int(end) - int(start)) > 0):
                #         print("ture")
                #         #convert the time into slots
                #         startSlot = slotsLookup.getStartSlot(start)
                #         endSlot = slotsLookup.getEndSlot(end)
                        
                #         #check if the slots already in the DB
                #         sql = 'SELECT slotID FROM UserAvailability WHERE userID="' + str(userid) + '" AND slotID>="' + str(startSlot) + '" AND slotID<="' + str(endSlot) + '" AND date ="' + form.cleaned_data['date'].strftime("%Y-%m-%d") + '";'
                #         print(sql)
                #         cursor.execute(sql)
                #         row = cursor.fetchall()
                #         if (len(row) != 0):
                #             print("Check")
                #             print(row)
                #             for i in row:
                #                 print (i[0])
                #             print("endcheck")
                #             slotsInDB = row

                #         #enter the form data into the DB
                #         sql = 'INSERT INTO UserAvailability (userID, date, slotID) value '
                #         for x in range(startSlot, endSlot+1, 1):
                #             slotValid = True
                #             print("current:", x)
                #             #skip if the slots already in the DB
                #             for i in slotsInDB:
                #                 if int(i[0]) == x:
                #                     print('Slots already in DB')
                #                     slotValid = False
                #             if slotValid == True:
                #                 sql = sql + '(' + str(userid) + ', "' + form.cleaned_data['date'].strftime("%Y-%m-%d") + '", ' + str(x) +'), '
                #         sql = sql[:-2] + ';'
                #         print(sql)    
                #         cursor.execute(sql)
                #         return HttpResponseRedirect('/calendar/')
                # else:
                #     print("invalid Date")
                #     """
                # end of code of the old version
            # else:
            #     print("invalid form")

            return render(request, 'calendar.html', {
                'group_list': grouplist,
                'username': request.user,
                'availableTimes': currentAvailableSlotsReturn,
                'startTime': period_start,
                'endTime': period_end,
                'duration': meetingLen,
                'no_of_meeting': numberOfMeet
            })
        return HttpResponse('<h1>ACCEESS DENIED</h1> <br> You are not allowed to be here, please contact an administrator if you think you should <br> <br><a href="/dashboard">return</a>', status=403)
    else:
        return HttpResponse('<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)


    ##the following code is for older version which uses RAW SQL Between if phase == 1: & context = {}


    # if 'userid' in request.session:
    #     print(slotsLookup.table[0][1])
    #     userid = request.session['userid']

    #     timetable = []
    #     slotsInDB = []
    #     currentAvailableSlots = []
    #     currentAvailableSlotsReturn = ''
    #     previousSlotID = -1
    #     previousSlottDateStr = '1970-1-1'

    #     period_start = period_end = datetime.datetime(1970, 1, 1, 0, 0, 0)
    #     meetingLen = numberOfMeet = 0

    #     db_conn = connections['default']
    #     cursor = db_conn.cursor()
    #     sql = 'SELECT date, slotID FROM UserAvailability WHERE userID="' + \
    #         str(userid) + '" ORDER BY date, slotID'
    #     cursor.execute(sql)
    #     row = cursor.fetchall()
    #     # print(len(row))
    #     timetable = row
    #     if len(timetable) != 0:
    #         for u in timetable:
    #             if u[0] == previousSlottDateStr:
    #                 if (previousSlotID + 1) == u[1]:
    #                     #print("Period Updated")
    #                     currentAvailableSlots[-1]['endslot'] = u[1]
    #                 else:
    #                     #print("newPeriod ", previousSlotID,"  ",u[1])
    #                     currentAvailableSlots.append(
    #                         {'date': u[0], 'startslot': u[1], 'endslot': u[1]})
    #             else:
    #                 previousSlottDateStr = u[0]
    #                # print("newDate")
    #                 currentAvailableSlots.append(
    #                     {'date': u[0], 'startslot': u[1], 'endslot': u[1]})
    #             previousSlotID = u[1]
    #             #print('Date:', u[0], ' Start Time:', slotsLookup.getStartTime(int(u[1])), ' End Time:', slotsLookup.getEndTime(int(u[1])))
    #         # print(currentAvailableSlots)
    #         for i in currentAvailableSlots:
    #             currentAvailableSlotsReturn = currentAvailableSlotsReturn + '<p> Date: ' + i['date'].strftime("%Y/%m/%d") + '&nbsp;&nbsp; ' + str(
    #                 slotsLookup.getStartTime(i['startslot'])) + ' - ' + str(slotsLookup.getEndTime(i['endslot'])) + ' </p> '
