from django import forms
from django.forms import ValidationError
from . import models

def validate_non_empty_list(value):
    if not isinstance(value, list) or len(value) < 1:
        raise ValidationError("The skills_required field must contain at least one skill.")

class  RecruitmentForm(forms.ModelForm): 
    job_details = forms.CharField(
        required=True, 
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40}) 
    )
    skills_required = forms.JSONField(initial=list, validators=[validate_non_empty_list])
    expected_salary = forms.IntegerField(required=True)
    minimum_experience = forms.IntegerField(required=True)
    class Meta:
        model = models.RecruitmentModel
        fields = "__all__"
    


