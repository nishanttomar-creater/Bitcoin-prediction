from django import forms

class formsubmit(forms.Form):
    s_date=forms.DateField()
    e_date=forms.DateField()
    s_time=forms.TimeField()
    e_time=forms.TimeField()
    