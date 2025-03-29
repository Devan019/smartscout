
from django.db import models
from django.forms import ValidationError

from myadmin.models import Manager
from employee.models import Profile

# Create your models here.
def validate_non_empty_list(value):
    if not isinstance(value, list) or len(value) < 1:
        raise ValidationError("The skills_required field must contain at least one skill.")


class Status(models.TextChoices):
    ACTIVE = "True", "Active"
    INACTIVE = "False", "Inactive"

from django.db import models
from myadmin.models import Manager  # ✅ Safe import

class RecruitmentModel(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name="recruitments", blank=True, null=True)
    job_details = models.TextField(blank=False, null=False)
    skills_required = models.JSONField(default=list)
    expected_salary = models.IntegerField(blank=False, null=False)
    minimum_experience = models.IntegerField(blank=False, null=False)
    form_status = models.BooleanField(default=True, blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True, blank=True, null=True)
    mailSent = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.job_details}"

    
class EmployeeModel(models.Model):
    EMPLOYEE_TYPES = (
        ('FR', 'Fresher'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('TL', 'Team Lead'),
        ('MGR', 'Manager'),
    )

    manager = models.OneToOneField(Manager, on_delete=models.CASCADE, related_name="employee_manager")
    profile = models.OneToOneField("employee.Profile", on_delete=models.CASCADE, related_name="employee_profile", blank=True, null=True)  # ✅ String reference
    experience = models.PositiveIntegerField(help_text="Years of experience")
    employee_type = models.CharField(max_length=3, choices=EMPLOYEE_TYPES)
    salary_lpa = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Salary (LPA)")
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.manager} - {self.employee_type}"