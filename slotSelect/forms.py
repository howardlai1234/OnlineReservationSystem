from django import forms


class GroupSelectForm(forms.Form):
    groupselect = forms.CharField(label='groupselect')
