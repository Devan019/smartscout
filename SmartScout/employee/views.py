from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from manager.models import RecruitmentModel
from employee.models import Profile
from employee.forms import ProfileForm

# Create your views here.
@login_required
def home(req):
  return render(req,"employee/home.html")

@login_required
def getForm(req):
  if(req.method == 'POST'):

    form = ProfileForm(req.POST, req.FILES)
    
    if form.is_valid():
      print("after valid")
      newPro = form.save(commit=False)
      newPro.user = req.user
      print(newPro.user.email)
      newPro.email = req.user.email
      newPro.save()
  
      return redirect("employee:home")
    
  try:
    exitPro = get_object_or_404(Profile, user = req.user.id)
    if exitPro:
      print("in")
      return render(req,"employee/profile.html", {
        'profile' : exitPro
      })
  except:
    return render(req,"employee/createCandidate.html")
  return render(req,"employee/createCandidate.html")


