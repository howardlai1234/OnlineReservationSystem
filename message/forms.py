from django import forms


class NameForm(forms.Form):
    receiver = forms.CharField(label='receiver', max_length=200)
    title = forms.CharField(label='title', max_length=200)
    body =  forms.CharField(label='body', max_length=200)
