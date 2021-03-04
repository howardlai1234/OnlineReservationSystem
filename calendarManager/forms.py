from django import forms

class NameForm(forms.Form):
    date = forms.DateField(label='date')
    startHour = forms.CharField(label='startHour')
    startMinute = forms.CharField(label='startMinute')
    endHour = forms.CharField(label='endHour')
    endMinute = forms.CharField(label='endMinute')