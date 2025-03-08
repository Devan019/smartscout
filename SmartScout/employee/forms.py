
from django import forms

from employee import models
from manager.forms import validate_non_empty_list


class  ProfileForm(forms.ModelForm): 
    
    profile_pic = forms.ImageField(required=False)
    name = forms.CharField(required=True)
    username = forms.CharField(disabled=True, required=False)
    email = forms.CharField(disabled=True,required=False)
    phone = forms.CharField(required=True)
    main_interest = forms.CharField(required=False)
    cpi = forms.FloatField(required=False)
    university = forms.CharField(required=False)
    skills_required = forms.JSONField(initial=list, validators=[validate_non_empty_list])
    experience = forms.IntegerField(required=False,min_value=0,max_value=60)
    resume = forms.FileField(required=False)

    class Meta:
        model = models.Profile
        fields = "__all__"