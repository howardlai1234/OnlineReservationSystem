from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from ORS.settings import DEBUG
from ORS.function import base_data
from config.models import Currentphase, Timetable
from dashboard.models import Slot, Groupdetail
from slotSelect.forms import GroupSelectForm, SlotSelectForm
from slotSelect.models import Selection
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        # variable for Access control check
        base_return = base_data(request.user)
        phase = base_return['phase']
        allowed_group = Timetable.objects.get().phase2_group_name
        userid = User.objects.get(username=request.user).pk
        group = User.objects.get(username=request.user).groups
        user_allowed_to_access = False

        # variable for generating slot list
        RegisteredSlotsReturn = []
        grouplist = ['All']
        cur_group = 'All'

        # for checking previous submit selection of user
        user_already_selected = {'flag': False}

        # mininum required length of a slot list
        min_required_length = 0

        # SelectionForm return message
        formError = ''
        formSuccess = ''
        failedSubmission = {'flag': False}

        if 'cur_group' in request.session:
            cur_group = request.session['cur_group']

        if DEBUG == True:
            phase = 2

        if phase == 2:
            for gp in request.user.groups.all():
                grouplist.append(gp.name)
                if gp.name == allowed_group:
                    user_allowed_to_access = True
        else:
            return HttpResponse(
                '<h1>ACCEESS DENIED</h1> <br> This feature is not available now, please check the scheudule<br><a href="/dashboard">return</a>', status=403) 
        if user_allowed_to_access == True:
            # request all available slots

            if request.method == "POST":
                if 'group_select' in request.POST:
                    form = GroupSelectForm(request.POST)
                    if form.is_valid():
                        cur_group = form.cleaned_data['groupselect']
                        request.session['cur_group'] = form.cleaned_data['groupselect']

                if 'slot_select' in request.POST:
                    form = SlotSelectForm(request.POST)

                    if form.is_valid():
                        valid = True
                        groupID = Group.objects.get(
                            name=form.cleaned_data['group']).pk
                        # split the form into list
                        SelectList_reurn = form.cleaned_data['selectionlist']
                        # SelectList_reurn = ''.join(SelectList_reurn.split())
                        # SelectList_reurn = SelectList_reurn.replace('\r', '')
                        # SelectList_reurn = SelectList_reurn.replace('\n', '')
                        slotSelectList = list(SelectList_reurn.split(","))

                        # check is all inputed value is integer
                        for t in slotSelectList:
                            if valid:
                                try:
                                    int(t)
                                except BaseException:
                                    formError = "Error: One of the selected item cannot be recognised"
                                    valid = False

                        # check if ther is duplicated slot
                        if valid:
                            for i in range(0, len(slotSelectList)):
                                for x in range(i + 1, len(slotSelectList)):
                                    if int(slotSelectList[i]) == int(
                                            slotSelectList[x]):
                                        valid = False
                                        formError = "Error: One item is repeated"

                        # check if all slot are allowed for this group
                        if valid:
                            allowed_slotID_for_this_group = Slot.objects.filter(
                                groupid=Group.objects.get(name=form.cleaned_data['group']).pk).all()
                            for i in slotSelectList:
                                slotID_exist_in_this_group = False
                                for s in allowed_slotID_for_this_group:
                                    if int(i) == s.slotid:
                                        slotID_exist_in_this_group = True
                                if slotID_exist_in_this_group == False:
                                    valid = False
                                    formError = "ERROR: At lease one of the slotID is invalid"

                        # check if the length of the list fits the minumium
                        # required length defined by group owner

                        if valid:
                            group_detail = Groupdetail.objects.filter(
                                groupid=groupID).get()
                            min_required_length = group_detail.min_required_slot
                            if min_required_length > len(slotSelectList):
                                valid = False
                                formError = "ERROR: Your list is too short, you must at least choose " + \
                                    str(min_required_length) + " slots"

                        # store it in DB if all check passed
                        if valid:
                            Selection.objects.filter(
                                groupid=groupID, userid=userid).delete()
                            for i in range(0, len(slotSelectList)):
                                Selection.objects.create(
                                    groupid=groupID,
                                    userid=userid,
                                    slotid=slotSelectList[i],
                                    userorder=i + 1,
                                    weightedscore=-1
                                )
                            formSuccess = "SUCCESS: your list is Saved"
                        else:
                            failedSubmission['flag'] = True
                            failedSubmission['list'] = SelectList_reurn

                        if DEBUG == True:
                            print("Selection Form Valid")
                            print('slotSelectList: ', slotSelectList)

            # generate the timetable list
            if cur_group == 'All':
                for gp in request.user.groups.all():
                    if Slot.objects.filter(groupid=Group.objects.get(
                            name=gp.name).pk).count() > 0:
                        Registered_slot_of_group = []
                        for s in Slot.objects.filter(
                                groupid=Group.objects.get(name=gp.name).pk).all():
                            Registered_slot_of_group.append(
                                {'id': s.slotid, 'start': s.starttime, 'end': s.endtime})
                        RegisteredSlotsReturn.append(
                            {'group': gp.name, 'slots': Registered_slot_of_group})
                if DEBUG == True:
                    print("RegisteredSlotsReturn: ", RegisteredSlotsReturn)
            else:

                Registered_slot_of_group = []
                groupid = Group.objects.get(name=cur_group).pk
                try:
                    available_slot_of_group = Slot.objects.filter(
                        groupid=groupid).all()
                    for s in available_slot_of_group:
                        Registered_slot_of_group.append(
                            {'id': s.slotid, 'start': s.starttime, 'end': s.endtime})
                    # Read the mininum required length of the group:
                    group_detail = Groupdetail.objects.filter(
                        groupid=groupid).get()
                except Slot.DoesNotExist:
                    return HttpResponse(
                        '<h1>No Slot Available for this group <br> <br><a href="/dashboard">Return</a>', status=401)
                except Groupdetail.DoesNotExist:
                    Groupdetail.objects.create(
                        groupid=groupid, min_required_slot=5)
                    group_detail = Groupdetail.objects.filter(
                        groupid=groupid).get()
                min_required_length = group_detail.min_required_slot

                # Read previous record of user submitted choice of that group
                RegisteredSlotsReturn.append(
                    {'group': cur_group, 'slots': Registered_slot_of_group})
                if 0 < Selection.objects.filter(
                        groupid=groupid, userid=userid).count():
                    user_already_selected['flag'] = True
                    user_already_selected['list'] = []
                    user_already_selected_list = Selection.objects.filter(
                        groupid=groupid, userid=userid).order_by('userorder').all()
                    for i in user_already_selected_list:
                        user_already_selected['list'].append(i.slotid)

            return render(request, 'selection.html', {
                'base_return': base_return,
                'formError': formError,
                'formSuccess': formSuccess,
                'currentGroup': cur_group,
                'grouplist': grouplist,
                'availableTimes': RegisteredSlotsReturn,
                'previousSelection': user_already_selected,
                'min_required_length': min_required_length,
                'failedSubmission': failedSubmission
            })
        else:
            return HttpResponse(
                '<h1>ACCEESS DENIED</h1> <br> You are not allowed to be here, please contact an administrator if you think you should <br> <br><a href="/dashboard">return</a>', status=403)
    else:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)
