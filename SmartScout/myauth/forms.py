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

  class Meta:
    model = CustomUser
    fields = ('username','email','password1','password2','role')

class AuthForm(AuthenticationForm):
  role = forms.ChoiceField(choices=ROLES,required=True,label="Role")
