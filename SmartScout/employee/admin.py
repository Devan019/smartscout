from django.contrib import admin

from employee.models import Profile,CandidateApplicationModel

# Register your models here.
admin.site.register(Profile)
admin.site.register(CandidateApplicationModel)