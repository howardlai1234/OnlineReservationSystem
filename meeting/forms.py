from django import forms


class ManageForm(forms.Form):
    meetingid = forms.CharField
    name = forms.CharField
    remark = forms.CharField
