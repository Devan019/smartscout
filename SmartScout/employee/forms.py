
from django import forms

from employee import models
from manager.forms import validate_non_empty_list


class  ProfileForm(forms.ModelForm): 
    
    profile_pic = forms.ImageField(required=False)
    name = forms.CharField(required=True)
    username = forms.CharField(disabled=True, required=False)
    email = forms.CharField(disabled=True,required=False)
    phone = forms.CharField(required=True)
    main_interest = forms.CharField(required=True)
    cpi = forms.FloatField(required=True)
    university = forms.CharField(required=True)
    skills_required = forms.JSONField(initial=list, validators=[validate_non_empty_list])
    experience = forms.IntegerField(required=False)
    resume = forms.FileField(required=True)

    class Meta:
        model = models.Profile
        fields = "__all__"


