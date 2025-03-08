from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from manager.models import RecruitmentModel
from employee.models import Profile
from employee.forms import ProfileForm
from manager.models import RecruitmentModel

# Create your views here.
@login_required
def home(req):
  return render(req,"employee/home.html")


@login_required
def getForm(req):
    if req.method == 'POST':
        form = ProfileForm(req.POST, req.FILES)
        if form.is_valid():
            print("after valid")
            newPro = form.save(commit=False)
            newPro.user = req.user
            print(newPro.user.email)
            newPro.email = req.user.email
            newPro.save()
            return redirect("employee:home")
    
    # Try to get existing profile for the user
    try:
        print('Checking for profile with email:', req.user.email)
        exitPro = Profile.objects.get(email=req.user.email)
        print('Found profile with ID:', exitPro.pk)
        return render(req, "employee/profile.html", {'profile': exitPro})
    except Profile.DoesNotExist:
        print('No profile found for email:', req.user.email)
        return render(req, "employee/createCandidate.html")
      
      
@login_required
def getJobs(req):
  jobs = RecruitmentModel.objects.all()
  active_jobs = []
  for job in jobs:
   if job.form_status == True:
     active_jobs.append(job)

  return render(req,"employee/jobs.html",{
    'jobs' : active_jobs
  })

@login_required
def updateProfile(req, id):
    print(str(id) + " " + str(req.user.id))
    empobj = get_object_or_404(Profile, user=req.user.id)
    
    if req.method == 'POST':
        form = ProfileForm(req.POST, req.FILES, instance=empobj)
        if form.is_valid():
            print('resume is', form.cleaned_data.get('resume'))
            skills = form.cleaned_data.get('skills_required')
            empobj.user = req.user
            empobj.skills_required = skills
            
            form.save()
            print('saved')
            return redirect('employee:createCandidate')
        else:
            print('invalid form')
            print(form.errors)
    
    form = ProfileForm(instance=empobj)
    return render(req, 'employee/updateEmployeeProfile.html', {'form': form, 'data': empobj})
