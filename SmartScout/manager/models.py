from django.db import models
from django.forms import ValidationError

# Create your models here.
def validate_non_empty_list(value):
    if not isinstance(value, list) or len(value) < 1:
        raise ValidationError("The skills_required field must contain at least one skill.")


class Status(models.TextChoices):
    ACTIVE = "True", "Active"
    INACTIVE = "False", "Inactive"

class RecruitmentModel(models.Model):
    job_details = models.TextField(blank=False, null=False)
    skills_required = models.JSONField(default=list,validators=[validate_non_empty_list])
    expected_salary = models.IntegerField(blank=False, null=False)
    minimum_experience = models.IntegerField(blank=False, null=False)
    form_status = models.BooleanField(default=Status.ACTIVE,blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True,blank=True, null=True)