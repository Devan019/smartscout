import string
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from myauth.models import CustomUser
from .forms import ManagerForm
from django.shortcuts import get_object_or_404
from .models import Manager, ManagerAuth
import random
from django.core.mail import send_mail
from django.conf import settings
from .messege import send_manager_email


def generate_auth_code():
    code = None
    while code is None or ManagerAuth.objects.filter(auth_code=code).exists():
        code = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))  
    return code

@login_required
def home(req):
  return render(req,"myadmin/home.html")

@login_required
def panel(req):
  managers = Manager.objects.all()
  return render(req,"myadmin/show_manager.html",{
    'managers' : managers
  })

@login_required
def createManager(req):
    print("add ma avyo",req.POST)
    if req.method == "POST":
      form = ManagerForm(req.POST)
      if form.is_valid():
          manager = form.save(commit=False) 
          auth_code = generate_auth_code()
          send_manager_email(manager.emailid,auth_code,manager.contact,manager.name)
          print("Saved:", manager)
          user = manager.save()
          ManagerAuth.objects.create(mid=manager, auth_code=auth_code)
          user1 = CustomUser()
          user1.role = 'manager'
          user1.username = manager.name
          user1.set_password(auth_code)
          user1.email = manager.emailid
          user1.save()
          
      return redirect("myadmin:panel")
    return render(req,'myadmin/add_manager_form.html')

@login_required
def updateManager(req,id=0):
  print("up avyo",req.POST,id)
  manager = get_object_or_404(Manager,id=id)
  if(req.method == "POST"):
    print("post ma")
    form = ManagerForm(req.POST,instance=manager)
    # print(form)
    if form.is_valid():
      form.save()
      print('saved')
    return redirect("myadmin:panel")
  # print('manager' , manager)
  return render(req,'myadmin/add_manager_form.html',{'manager':manager})
 
@login_required
def deleteManager(req,id):
  manager = get_object_or_404(Manager,id=id)
  try:
      user = CustomUser.objects.get(username=manager.name)
      print(f"Deleting CustomUser: {user}")
      user.delete()
  except CustomUser.DoesNotExist:
      print("CustomUser not found!")
  manager.delete()
  print("thai vyo delete")
  return redirect("myadmin:panel")
  

