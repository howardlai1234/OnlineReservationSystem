from django import forms

class NameForm(forms.Form):
    date = forms.DateField(label='date')
    startHour = forms.CharField(label='startHour')
    startMinute = forms.DecimalField(label='startMinute')
    meetingLength = forms.DecimalField(label='meetingLength')
    numberOfMeeting = forms.DecimalField(label='numberOfMeeting')