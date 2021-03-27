from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from ORS.settings import DEBUG
from config.models import Currentphase, Timetable
from dashboard.models import Slot
from slotSelect.forms import GroupSelectForm, SlotSelectForm
from slotSelect.models import Selection
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        #variable for Access control check
        phase = Currentphase.objects.get().phase
        allowed_group = Timetable.objects.get().phase2_group_name
        userid = User.objects.get(username=request.user).pk
        group = User.objects.get(username=request.user).groups
        user_allowed_to_access = False
        

        #variable for generating slot list
        RegisteredSlotsReturn = []
        grouplist = ['All']
        cur_group = 'All'

        #for checking previous submit selection of user
        user_already_selected = {'flag': False}

        #SelectionForm return message
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
        if user_allowed_to_access == True:

            # request all available slots

            # Reserve for viewiing all group slots


            if request.method == "POST":
                if 'group_select' in request.POST:
                    form = GroupSelectForm(request.POST)
                    if form.is_valid():
                        print(form.cleaned_data['groupselect'])
                        cur_group = form.cleaned_data['groupselect']
                        request.session['cur_group'] = form.cleaned_data['groupselect']

                        #temp. move here to prevent bug
                        
                if 'slot_select' in request.POST:
                    form = SlotSelectForm(request.POST)
                    if form.is_valid():
                        valid = True

                        #split the form into list
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
                                except:
                                    formError = "Error: One of the selected item cannot be recognised"
                                    valid = False

                        # check if ther is duplicated slot
                        if valid:
                            for i in range(0, len(slotSelectList)):
                                for x in range(i + 1, len(slotSelectList)):
                                    if int(slotSelectList[i]) == int(slotSelectList[x]):
                                        valid = False
                                        formError = "Error: One item is repeated"
                        
                        #check if all slot are balid for this group
                        if valid:
                            allowed_slotID_for_this_group = Slot.objects.filter(groupid=Group.objects.get(name=form.cleaned_data['group']).pk).all()
                            for i in slotSelectList:
                                slotID_exist_in_this_group = False
                                for s in allowed_slotID_for_this_group:
                                    if int(i) == s.slotid:
                                        slotID_exist_in_this_group = True
                                if slotID_exist_in_this_group == False:
                                    valid = False
                                    formError = "ERROR: At lease one of the slotID is invalid"

                        #store it in DB if all check passed
                        if valid:
                            groupid = Group.objects.get(name=gp.name).pk
                            Selection.objects.filter(groupid=groupid, userid=userid).delete()
                            for i in range(0, len(slotSelectList)):
                                Selection.objects.create(
                                    groupid = groupid,
                                    userid = userid,
                                    slotid = slotSelectList[i],
                                    userorder = i + 1,
                                    weightedscore = -1
                                )
                            formSuccess = "SUCCESS: your list is Saved"
                        else:
                            failedSubmission['flag'] = True
                            failedSubmission['list'] = SelectList_reurn

                        if DEBUG == True:
                            print("Selection Form Valid")
                            print('slotSelectList: ', slotSelectList)
            
            #generate the timetable list
            Registered_slot_of_group = []
            if cur_group == 'All':
                for gp in request.user.groups.all():
                    if Slot.objects.filter(groupid=Group.objects.get(name=gp.name).pk).count() > 0:
                        for s in Slot.objects.filter(groupid=Group.objects.get(name=gp.name).pk).all():
                            Registered_slot_of_group.append({'id': s.slotid, 'start': s.starttime, 'end': s.endtime})
                        RegisteredSlotsReturn.append({'group': gp.name, 'slots': Registered_slot_of_group})
            else:
                groupid = Group.objects.get(name=cur_group).pk
                for s in Slot.objects.filter(groupid=groupid).all():
                    Registered_slot_of_group.append(
                        {'id': s.slotid, 'start': s.starttime, 'end': s.endtime})
                RegisteredSlotsReturn.append(
                    {'group': cur_group, 'slots': Registered_slot_of_group})
                if 0 < Selection.objects.filter(groupid=groupid, userid=userid).count():
                    user_already_selected['flag'] = True
                    user_already_selected['list'] = []
                    user_already_selected_list = Selection.objects.filter(groupid=groupid, userid=userid).order_by('userorder').all()
                    for i in user_already_selected_list:
                        user_already_selected['list'].append(i.slotid)

            
            return render(request, 'selection.html', {
                'formError': formError,
                'formSuccess':  formSuccess,
                'currentGroup': cur_group,
                'grouplist': grouplist,
                'availableTimes': RegisteredSlotsReturn,
                'previousSelection': user_already_selected,
                'failedSubmission': failedSubmission
            })
                
        else:
            return HttpResponse(
                '<h1>ACCEESS DENIED</h1> <br> You are not allowed to be here, please contact an administrator if you think you should <br> <br><a href="/dashboard">return</a>', status=403)
    else:
        return HttpResponse(
            '<h1>ACCEESS DENIED</h1> <br> Please Login first <br> <br><a href="/login">Login</a>', status=401)
