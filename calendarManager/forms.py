from django import forms


class NameForm(forms.Form):
    group = forms.CharField(label='group')
    date = forms.DateField(label='date')
    startHour = forms.CharField(label='startHour')
    startMinute = forms.DecimalField(label='startMinute')
    meetingLength = forms.DecimalField(label='meetingLength')
    numberOfMeeting = forms.DecimalField(label='numberOfMeeting')

class ConfirmForm(forms.Form):
    group = forms.CharField(label='confirm_group')
    startTime = forms.CharField(label='confirm_startTime')
    meetingLength = forms.CharField(label='confirm_duration')
    numberOfMeeting = forms.CharField(label='confirm_no_of_meeting')