from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from .models import CustomUser

ROLES = (
    ('employee', 'Employee'),
    ('manager', 'Manager'),
    ('admin', 'Admin'),
  )
class UserForm(UserCreationForm):

  email = forms.EmailField(max_length=100)
  role = forms.ChoiceField(choices=ROLES,required=False,)
  authCode = forms.CharField(max_length=6,required=False)

  class Meta:
    model = CustomUser
    fields = ('username','email','password1','password2','role','authCode')

class AuthForm(AuthenticationForm):
  role = forms.ChoiceField(choices=ROLES,required=True,label="Role")
  authCode = forms.CharField(max_length=6,required=False,label="authication code")