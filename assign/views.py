from munkres import Munkres, print_matrix, make_cost_matrix, DISALLOWED
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.contrib.auth.models import User, Group
from dashboard.models import Groupdetail, Meeting, Slot
from slotSelect.models import Selection
from message.views import sent_new_message
from ORS.settings import DEBUG
# Create your views here.

D = DISALLOWED


def home(request):
    # Access control measure
    if not request.user.is_authenticated:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)
    if not request.user.is_superuser:
        return HttpResponse('<h1>ACCEESS DENIED</h1>', status=404)

    for gp in Group.objects.all():
        groupID = Group.objects.get(name=gp.name).pk
        if DEBUG:
            print('Group Name:', gp.name, 'Group id:', groupID)
        selection = Selection.objects.filter(
            groupid=groupID).order_by(
            'userid', 'slotid')
        available_slot_lookup = []
        userid_lookup = []
        for a in Slot.objects.filter(groupid=groupID).order_by('slotid'):
            available_slot_lookup.append(a.slotid)
        if DEBUG:
            print("Available slots: ", available_slot_lookup)
        last_userid = 0
        matrix = []
        selection_dict = {}
        for s in selection:
            if s.userid == last_userid:
                selection_dict[s.slotid] = s.userorder
            else:
                if last_userid != 0:
                    # if DEBUG:
                    #    print("selection dict", selection_dict)
                    row_constr_return = matrix_row_constructor(
                        available_slot_lookup, selection_dict)
                    if row_constr_return['flag']:
                        matrix.append(row_constr_return['list'])
                selection_dict = {}
                last_userid = s.userid
                userid_lookup.append(s.userid)
                print("userID:", s.userid)
                selection_dict[s.slotid] = s.userorder
        #print("selection dict", selection_dict)
        row_constr_return = matrix_row_constructor(
            available_slot_lookup, selection_dict)
        if row_constr_return['flag']:
            matrix.append(row_constr_return['list'])
        m = Munkres()
        matrix_empty = False
        # try:
        if len(matrix) > 0:
            indexes = m.compute(matrix)
            # except UnsolvableMatrix:
            #print("empty matrix")
            #matrix_empty = True
            # if not matrix_empty:
            confirm_list = []
            if DEBUG:
                print("Matrix of Group:", gp.name)
                print_matrix(matrix)
                print("")
                total = 0
                print('index:', indexes)
            for row, column in indexes:
                value = matrix[row][column]
                total += value
                confirm_list.append({'group': groupID,
                                     'userid': userid_lookup[row],
                                     'slot': available_slot_lookup[column]})
                if DEBUG:
                    print(
                        f'(user:{userid_lookup[row]}, slot:{available_slot_lookup[column]}) -> {value}')
            if DEBUG:
                print(f'total cost: {total}')
                print("userlist: ", userid_lookup)
                print("slotlist: ", available_slot_lookup)
            batch_add_meeting(confirm_list)

    # for usr in User.objects.all():
    #    print ("username:", usr.username, "id:", User.objects.get(username=usr.username).pk)

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
    # print('index:', indexes)
    # for row, column in indexes:
    #    value = matrix[row][column]
    #    total += value
    #    print(f'({row}, {column}) -> {value}')
    # print(f'total cost: {total}')

    return HttpResponse("Hello")


def matrix_row_constructor(available_slot_list, user_selection_dict):
    # print("available:",available_slot_list,"user:",user_selection_dict)
    return_list = []
    valid_input = False
    for i in available_slot_list:
        if i in user_selection_dict:
            return_list.append(user_selection_dict[i])
            valid_input = True
        else:
            return_list.append(DISALLOWED)
    #print("return_list:", return_list)
    return {'flag': valid_input, 'list': return_list}


def batch_add_meeting(meeting_detail):
    for meeting in meeting_detail:
        slot_detail = Slot.objects.filter(slotid=meeting['slot']).get()
        Meeting.objects.create(
            hostid=slot_detail.ownerid,
            participantid=meeting['userid'],
            date=slot_detail.starttime.date(),
            starttime=slot_detail.starttime.time(),
            endtime=slot_detail.endtime.time(),
            name=str(Group.objects.get(id=meeting['group']).name) + " Meeting",
            remark="N/A",
            statusid=1
        )
        meeting_id = Meeting.objects.get(
            hostid=slot_detail.ownerid,
            participantid=meeting['userid'],
            date=slot_detail.starttime.date(),
            starttime=slot_detail.starttime.time(),
            endtime=slot_detail.endtime.time(),
            name=str(Group.objects.get(id=meeting['group']).name) + " Meeting",
            remark="N/A",
            statusid=1
        ).pk
        # sent new message to participant
        hostname = User.objects.get(id=slot_detail.ownerid).username
        participantname = User.objects.get(id=meeting['userid']).username
        sent_new_message(
            0,
            meeting['userid'],
            0,
            meeting_id,
            "A new meeting is generated",
            "A new meeting is generated by the system for meeting of " + str(Group.objects.get(
                id=meeting['group']).name) + ",between " + hostname + " and " + participantname + " please check it in meeting page for details"
        )
        # sent new meeting message to host
        sent_new_message(
            0,
            slot_detail.ownerid,
            0,
            meeting_id,
            "A new meeting is generated",
            "A new meeting is generated by the system for meeting of " + str(Group.objects.get(
                id=meeting['group']).name) + ",between " + hostname + " and " + participantname + " please check it in meeting page for details"
        )
        print(
            "Slots detail:",
            slot_detail.ownerid,
            slot_detail.starttime,
            slot_detail.endtime,
        )
