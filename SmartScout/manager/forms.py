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
    
class EmployeeForm(forms.ModelForm):
    EMPLOYEE_TYPES = (
        ('FR', 'Fresher'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('TL', 'Team Lead'),
        ('MGR', 'Manager'),
    )
    role=forms.CharField(max_length=100)
    experience = forms.IntegerField(help_text="Years of experience")
    employee_type = forms.ChoiceField(choices=EMPLOYEE_TYPES)
    salary_lpa = forms.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = models.EmployeeModel  # This was missing
        fields = ['experience', 'role', 'employee_type', 'salary_lpa'] 


