from django import forms


class GroupSelectForm(forms.Form):
    groupselect = forms.CharField(label='groupselect')


class SlotSelectForm(forms.Form):
    A1 = forms.IntegerField(label='A1')
    A2 = forms.IntegerField(label='A2')
    A3 = forms.IntegerField(label='A3')
    B1 = forms.IntegerField(label='B1')
    B2 = forms.IntegerField(label='B2')
    B3 = forms.IntegerField(label='B3')
    B4 = forms.IntegerField(label='B4')
    B5 = forms.IntegerField(label='B5')
    C1 = forms.IntegerField(label='C1')
    C2 = forms.IntegerField(label='C2')
    C3 = forms.IntegerField(label='C3')
    C4 = forms.IntegerField(label='C4')
    C5 = forms.IntegerField(label='C5')
    C6 = forms.IntegerField(label='C6')
    C7 = forms.IntegerField(label='C7')
