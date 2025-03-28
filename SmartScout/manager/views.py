
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from employee.models import CandidateApplicationModel, Profile
from .models import RecruitmentModel, Status
from myadmin.models import Manager
from .forms import RecruitmentForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
import json
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
      print( req.user.id, req.user.email)
      manager = Manager.objects.get(emailid = req.user.email)
      recruitment = form.save(commit=False)
      recruitment.manager = manager
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
    try:
      manager = Manager.objects.get(emailid=req.user.email)
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

      recobj.manager = Manager.objects.get(emailid=req.user.email)

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

@login_required
def showApplications(request, id):
    try:
       
        recruitment = RecruitmentModel.objects.get(id=id)
       
      
        applications = CandidateApplicationModel.objects.filter(recruitment=recruitment)

        
        profiles_data = []
        
        for application in applications:
            

            required_skills = set(recruitment.skills_required)
            profile_skills = set(application.profile.skills_required)
            matched_skills = list(required_skills.intersection(profile_skills))
            match_percentage = (len(matched_skills) / len(required_skills)) * 100 if required_skills else 0
            
            exp_diff = application.profile.experience - recruitment.minimum_experience
            
            profiles_data.append({
                'app_id' : application.id,
                'user_id': application.user.id,
                'username': application.user.username,
                'profile_id': application.profile.id,
                'matched_skills': matched_skills,
                'match_percentage': round(match_percentage, 2),
                'experience_diff': exp_diff,
                'profile_experience': application.profile.experience,
                'required_experience': recruitment.minimum_experience,
                'profile': application.profile, 
                'status': application.status
            })

            

        profiles_sorted_by_skills = sorted(
            profiles_data,
            key=lambda x: (-x['match_percentage'], -x['experience_diff'])
        )

        profiles_sorted_by_experience = sorted(
            profiles_data,
            key=lambda x: (-x['experience_diff'], -x['match_percentage'])
        )

        filter_type = request.GET.get('filter', 'all')
    
        if filter_type == 'skills':
          profiles_data = profiles_sorted_by_skills 
        elif filter_type == 'exp':
          profiles_data = profiles_sorted_by_experience 
        else:
          profiles_data = profiles_data  
        
        
        
        
        
        context = {
            'recruitment': recruitment,
            'profiles': profiles_data,
            'profiles_by_skills': profiles_sorted_by_skills,
            'profiles_by_experience': profiles_sorted_by_experience,
            'job_title': recruitment.job_details[:50] + '...' if recruitment.job_details else ''
        }

       
        
        return render(request, "manager/sortedProfiles.html", context)
    
    except RecruitmentModel.DoesNotExist:
        return render(request, "404.html", status=404)


@login_required
def showProfile(req, id):
    print(id)
    profile = get_object_or_404(Profile, id=id)
    return render(req, "manager/showProfile.html",{
       'profile' : profile
    })

@login_required
def process_application(request, application_id):
    print(application_id , " id got it")
    application = get_object_or_404(CandidateApplicationModel, id=application_id)
    print("application is found ", application)
    recruitment_id=application.recruitment.id
    action = request.POST.get('action')
    print("action is found ", action)
    if action == 'accept':
        application.status = 'ACCEPTED'
    elif action == 'reject':
        application.status = 'REJECTED'
    elif action == 'pending':
        application.status = 'PENDING'
    
    application.save()
    return redirect("manager:applications",id=recruitment_id)

@login_required
def showsStatusApplications(req, id):
   print(req.user.id)
   manager = Manager.objects.get(emailid=req.user.email)
   
   recruitments = RecruitmentModel.objects.filter(manager=manager)
   recruitment = get_object_or_404(RecruitmentModel, id=id)


   print(recruitments , " get it")
   return render(req,"manager/showApplicationsStatus.html",{
      'recruitments': recruitments,
      'current_recruitment' : recruitment
   })

@login_required
def showsDeafultStatusApplications(req):
  manager = Manager.objects.get(emailid=req.user.email)
   
  recruitments = RecruitmentModel.objects.filter(manager=manager)
  recruitment = recruitments.first()
  applications = CandidateApplicationModel.objects.filter(recruitment=recruitment)

        
  profiles_data = []
        
  for application in applications:
            

    required_skills = set(recruitment.skills_required)
    profile_skills = set(application.profile.skills_required)
    matched_skills = list(required_skills.intersection(profile_skills))
    match_percentage = (len(matched_skills) / len(required_skills)) * 100 if required_skills else 0
    
    exp_diff = application.profile.experience - recruitment.minimum_experience
    
    profiles_data.append({
        'app_id' : application.id,
        'user_id': application.user.id,
        'username': application.user.username,
        'profile_id': application.profile.id,
        'matched_skills': matched_skills,
        'match_percentage': round(match_percentage, 2),
        'experience_diff': exp_diff,
        'profile_experience': application.profile.experience,
        'required_experience': recruitment.minimum_experience,
        'profile': application.profile, 
        'status': application.status
    })

            

  profiles_sorted_by_skills = sorted(
      profiles_data,
      key=lambda x: (-x['match_percentage'], -x['experience_diff'])
  )

  profiles_sorted_by_experience = sorted(
      profiles_data,
      key=lambda x: (-x['experience_diff'], -x['match_percentage'])
  )

  filter_type = req.GET.get('filter', 'all')
    
  if filter_type == 'skills':
    profiles_data = profiles_sorted_by_skills 
  elif filter_type == 'exp':
    profiles_data = profiles_sorted_by_experience 
  else:
    profiles_data = profiles_data  
            
  context = {
      'recruitment': recruitment,
      'profiles': profiles_data,
      'profiles_by_skills': profiles_sorted_by_skills,
      'profiles_by_experience': profiles_sorted_by_experience,
      'job_title': recruitment.job_details[:50] + '...' if recruitment.job_details else ''
  }

       

  print(recruitments , " get it")
  return render(req,"manager/showApplicationsStatus.html",{
     'recruitments': recruitments,
     'current_recruitment' : recruitment,
     'applications' : applications,
     'context' : context
  })


