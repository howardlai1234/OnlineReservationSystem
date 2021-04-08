from django import forms


class ManageForm(forms.Form):
    meetingid = forms.CharField()
    name = forms.CharField()
    date = forms.DateField()
    starttime = forms.TimeField()
    endtime = forms.TimeField()
    remark = forms.CharField()
