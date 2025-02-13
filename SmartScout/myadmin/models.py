from django.db import models
from django.core.validators import MinLengthValidator
import random

def generate_auth_code():
    return str(random.randint(100000, 999999))

class Manager(models.Model):
    name = models.CharField(max_length=255,default='')
    emailid = models.EmailField(unique=True)
    contact = models.CharField(max_length=15, null=False, blank=False)
    auth_code = models.CharField(max_length=6, validators=[MinLengthValidator(6)],unique=True, default=generate_auth_code)

    def __str__(self):
        return self.name
