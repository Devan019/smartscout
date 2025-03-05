from django.shortcuts import get_object_or_404, redirect, render
from .models import RecruitmentModel, Status
from .forms import RecruitmentForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(req):
  return render(req,"manager/home.html")

@login_required
def generateRecruitmentForm(req, id = 0):
  print("i ")
  reqform = get_object_or_404(RecruitmentModel, id)
  if req.method == 'POST':
    form = RecruitmentForm(req.POST)
    print("in post")
    exitform = RecruitmentForm(req.POST, instance=reqform)
  
    if form.is_valid():
      print("valid ")
      form.save()
      print("saved")
      return redirect("manager:readForms")
    
    
    print(":not valid ", form)
    
  # form = RecruitmentForm()
  return render(req,'manager/generateRecruitmentForm.html',{
    form: exitform
  })

@login_required
def getRecruitmentForm(req):
  forms = RecruitmentModel.objects.all()
  return render(req,"manager/showrecruitmentForms.html",{
    'jobs': forms
  })

@login_required
def doDeactivate(req, id):
  form = get_object_or_404(RecruitmentModel, id = id)
  form.form_status = Status.INACTIVE
  form.save()
  return redirect("manager:readForms")

@login_required
def doActivate(req, id):
  form = get_object_or_404(RecruitmentModel, id = id)
  form.form_status = Status.ACTIVE
  form.save()
  return redirect("manager:readForms")

  
  