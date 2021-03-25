from django import forms


class NameForm(forms.Form):
    group = forms.CharField(label='group')
    date = forms.DateField(label='date')
    startHour = forms.CharField(label='startHour')
    startMinute = forms.DecimalField(label='startMinute')
    meetingLength = forms.DecimalField(label='meetingLength')
    numberOfMeeting = forms.DecimalField(label='numberOfMeeting')

class ConfirmForm(forms.Form):
    confirm_group = forms.CharField(label='confirm_group')
    confirm_startTime = forms.CharField(label='confirm_startTime')
    confirm_duration = forms.IntegerField(label='confirm_duration')
    confirm_no_of_meeting = forms.IntegerField(label='confirm_no_of_meeting')