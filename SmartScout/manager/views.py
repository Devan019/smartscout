from django.shortcuts import redirect, render
from .models import RecruitmentModel
from .forms import RecruitmentForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(req):
  return render(req,"manager/home.html")

@login_required
def generateRecruitmentForm(req):
  print("i ")
  if req.method == 'POST':
    form = RecruitmentForm(req.POST)
    print("in post")
  
    if form.is_valid():
      print("valid ")
      form.save()
      print("saved")
      return redirect("manager:readForms")
    print(":not valid")
    
  # form = RecruitmentForm()
  return render(req,'manager/generateRecruitmentForm.html')

@login_required
def getRecruitmentForm(req):
  forms = RecruitmentModel.objects.all()
  return render(req,"manager/showrecruitmentForms.html",{
    'jobs': forms
  })
  
  