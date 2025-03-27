from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from myauth.models import CustomUser
from manager.models import RecruitmentModel
from .models import CandidateApplicationModel, Profile
from .forms import ProfileForm
from manager.models import RecruitmentModel
from .pdfScan import process_resume

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
    profileobj = get_object_or_404(Profile,user = req.user.id)
  return render(req,"employee/jobs.html",{
    'jobs' : active_jobs,
    'profile':profileobj
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


@login_required
def upload_resume(request):
    if request.method == "POST" and request.FILES.get("resume"):
        uploaded_file = request.FILES["resume"]
        extracted_data = process_resume(uploaded_file)
        
        if extracted_data:
            return JsonResponse({
                "skills": extracted_data["skills"],
                "contact": extracted_data["contact"][0] if extracted_data["contact"] else "",
                "email": extracted_data["email"][0] if extracted_data["email"] else "",
            })
    
    return JsonResponse({"error": "Invalid file or extraction failed."})


@login_required
def applyForJob(req,id):
    recruitObj = get_object_or_404(RecruitmentModel,id = id)
    
    empObj = get_object_or_404(Profile, user=req.user.id)
    jobObj = CandidateApplicationModel()
    user = CustomUser.objects.get(pk=req.user.id)
    jobObj.profile = empObj
    print(jobObj.profile)
    jobObj.user = user
    print(jobObj.user)
    
    jobObj.recruiment = recruitObj
    print(jobObj.recruiment)

    jobObj.save()
    if jobObj.id:
        empObj.jobsApplied.add(recruitObj)
    return redirect("employee:jobs")
