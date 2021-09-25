from django import forms
from MDAT import models

class roll_no(forms.Form):
    roll_no = forms.CharField(required=False)
