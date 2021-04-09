from django import forms


class ManageForm(forms.Form):
    meetingid = forms.CharField()
    name = forms.CharField()
    date = forms.DateField()
    starttime = forms.TimeField()
    endtime = forms.TimeField()
    remark = forms.CharField()


class CreateForm(forms.Form):
    name = forms.CharField()
    date = forms.DateField()
    starttime = forms.TimeField()
    endtime = forms.TimeField()
    host = forms.CharField()
    participant = forms.CharField()
    remark = forms.CharField()
