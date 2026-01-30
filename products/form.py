from django import forms
from . models import pish_sabt

class pishSabtForm(forms.ModelForm):
    class Meta:
        model = pish_sabt
        fields = ['product_choice','std_name','std_lastname','age','parent_name','mobile','desc']