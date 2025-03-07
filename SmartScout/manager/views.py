from django.shortcuts import get_object_or_404, redirect, render
from .models import RecruitmentModel, Status
from myadmin.models import Manager
from .forms import RecruitmentForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(req):
  return render(req,"manager/home.html")

@login_required
def generateRecruitmentForm(req, id = 0):

  print("i ")
  if req.method == 'POST':
    form = RecruitmentForm(req.POST)
    print("in post")  
    if form.is_valid():
      print("valid "+str(req.user.id) + req.user.username)
      recruitment = form.save(commit=False)  
      recruitment.manager = Manager.objects.get(id=req.user.id)
      recruitment.save()
      print("saved")
      return redirect("manager:readForms")
    else:
      print(form.error_class)
    
    
    print(":not valid ")
    
  form = RecruitmentForm()
  return render(req,'manager/generateRecruitmentForm.html',{
    'form': form
  })

@login_required
def getRecruitmentForm(req):
    # Ensure req.user is a Manager instance
    try:
      manager = Manager.objects.get(id=req.user.id)
    except Manager.DoesNotExist:
        manager = None  # Handle the case where the user is not a manager

    if manager:
        active_forms = RecruitmentModel.objects.filter(form_status=True, manager=manager)
        inactive_forms = RecruitmentModel.objects.filter(form_status=False, manager=manager)
    else:
        active_forms = RecruitmentModel.objects.none()
        inactive_forms = RecruitmentModel.objects.none()

    return render(req, "manager/showrecruitmentForms.html", {
        'active_jobs': active_forms,
        'deactivated_jobs': inactive_forms,
        'user_id': req.user.id
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

  
@login_required
def updateRecruitmentForm(req,id):
  recobj = get_object_or_404(RecruitmentModel, id = id)
  print(recobj.manager)
  if req.method == 'POST':
    form = RecruitmentForm(req.POST,instance = recobj)
    if form.is_valid():
      print("form updated")
      skills_data = form.cleaned_data.get('skills_required', [])

      recobj.manager = Manager.objects.get(id=req.user.id)

      recobj.skills_required = skills_data

      recobj.save()

      skills_data = form.cleaned_data.get('skills_required', [])
      print(skills_data)
    else:
      print('form invalid update')
    return redirect('manager:readForms')
  form = RecruitmentForm(instance=recobj)

  print(recobj.skills_required)
  return render(req,'manager/updateRecruitmentForm.html',{'form':form,'data':recobj})

@login_required
def deleteRecruitmentForm(req,id):
  recobj = get_object_or_404(RecruitmentModel,id = id)
  recobj.delete()
  return redirect('manager:readForms')

    

