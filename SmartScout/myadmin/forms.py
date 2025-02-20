from django import forms
from .models import Manager


class ManagerForm(forms.ModelForm): 
    name = forms.CharField(max_length=255, required=True) 
    emailid = forms.EmailField(max_length=255)
    contact = forms.CharField(max_length=12,required=True)  
    auth_code = forms.CharField(max_length=8, min_length=8, required=False)

    class Meta:
        model = Manager
        fields = ['name', 'emailid', 'contact']
