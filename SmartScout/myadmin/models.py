from django.db import models
from django.core.validators import MinLengthValidator



class Manager(models.Model):
    name = models.CharField(max_length=255,default='')
    emailid = models.EmailField(unique=True)
    contact = models.CharField(max_length=15, null=False, blank=False)

    def __str__(self):
        return str(self.id) + ' ' + self.name

class ManagerAuth(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, name="mid")
    auth_code = models.CharField(max_length=8, validators=[MinLengthValidator(8)],unique=True,)
    def __str__(self):
        return self.auth_code
    