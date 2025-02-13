from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import ManagerForm
from django.shortcuts import get_object_or_404
from .models import Manager
import random

def generate_auth_code():
    return str(random.randint(100000, 999999))

@login_required
def home(req):
  return render(req,"myadmin/home.html")

@login_required
def panel(req):
  return render(req,"myadmin/manages.html")

@login_required
def createManager(req):
    print(req.POST)
    if req.method == "POST":
        form = ManagerForm(req.POST)
        if form.is_valid():
            manager = form.save(commit=False) 
            manager.auth_code = generate_auth_code()
            manager.save()
            print("Saved:", manager)
    return redirect("myadmin:panel")


def updateManager(req,id):
  manager = get_object_or_404(Manager,id=id)
  if(req.method == "POST"):
    
    manager = ManagerForm(req.POST)
    manager.save()
    print(manager)

  return redirect("panel")

def getAllManagers(req):
  managers = get_object_or_404(Manager)
  return render(req,"myadmin/manages.html",{
    'managers' : managers
  })

def deleteManager(req,id):
  manager = get_object_or_404(Manager,id=id)
  manager.delete()
  return redirect("panel")
  

