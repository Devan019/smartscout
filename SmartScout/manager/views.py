
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render

from employee.models import CandidateApplicationModel, Profile
from manager.accepted import get_acceptance_email
from manager.rejection import get_rejection_email
from .models import EmployeeModel, RecruitmentModel, Status, TeamModel
from myadmin.models import Manager
from .forms import EmployeeForm, RecruitmentForm, TeamForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
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
    return redirect("manager:getApplication",id=recruitment_id)

def sendingObject(req, recruitment, recruitments):
    applications = CandidateApplicationModel.objects.filter(recruitment=recruitment)
    
    profiles_data = []
    
    for application in applications:
        required_skills = set(recruitment.skills_required)
        profile_skills = set(application.profile.skills_required)
        matched_skills = list(required_skills.intersection(profile_skills))
        match_percentage = (len(matched_skills) / len(required_skills)) * 100 if required_skills else 0
        
        exp_diff = application.profile.experience - recruitment.minimum_experience
        
        profiles_data.append({
            'app_id': application.id,  
            'user_id': application.user.id,
            'username': application.user.username,
            'profile_id': application.profile.id,
            'matched_skills': matched_skills,
            'match_percentage': round(match_percentage, 2),
            'experience_diff': exp_diff,
            'profile_experience': application.profile.experience,
            'required_experience': recruitment.minimum_experience,
            'profile': application.profile,
            'status': application.status,
            'application': application  # Include the full application object
        })

    # Sorting logic remains the same
    profiles_sorted_by_skills = sorted(profiles_data, key=lambda x: (-x['match_percentage'], -x['experience_diff']))
    profiles_sorted_by_experience = sorted(profiles_data, key=lambda x: (-x['experience_diff'], -x['match_percentage']))

    # Filtering
    filter_type = req.GET.get('filter', 'all')
    status_filter = req.GET.get('status')
    
    if filter_type == 'skills':
        profiles_data = profiles_sorted_by_skills
    elif filter_type == 'exp':
        profiles_data = profiles_sorted_by_experience
    
    if status_filter and status_filter.upper() in ['ACCEPTED', 'PENDING']:
        profiles_data = [p for p in profiles_data if p['status'] == status_filter.upper()]

    return render(req, "manager/showApplicationsStatus.html", {
        'recruitments': recruitments,
        'current_recruitment': recruitment,
        'applications': applications,
        'recruitment': recruitment,
        'profiles': profiles_data,
        'profiles_by_skills': profiles_sorted_by_skills,
        'profiles_by_experience': profiles_sorted_by_experience,
        'job_title': recruitment.job_details[:50] + '...' if recruitment.job_details else ''
    })

@login_required
def showsStatusApplications(req, id):
   print(req.user.id)
   manager = Manager.objects.get(emailid=req.user.email)
   
   recruitments = RecruitmentModel.objects.filter(manager=manager)
   recruitment = get_object_or_404(RecruitmentModel, id=id)
   return sendingObject(req, recruitment, recruitments)

@login_required
def showsDeafultStatusApplications(req):
  manager = Manager.objects.get(emailid=req.user.email)
   
  recruitments = RecruitmentModel.objects.filter(manager=manager)
  recruitment = recruitments.first()
  return sendingObject(req, recruitment, recruitments)

def send_rejection_email(recruitment_name, candidate_name, candidate_email):
    print(recruitment_name, candidate_name, candidate_email)
    email_body = get_rejection_email(recruitment_name, candidate_name, candidate_email)
    
    email = EmailMessage(
        subject=f"Update on your application for {recruitment_name}",
        body=email_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[candidate_email],
    )
    email.content_subtype = "html"
    email.send()

def send_acceptance_email(recruitment_name, candidate_name, candidate_email, next_steps):
    print(recruitment_name, candidate_name, candidate_email)
    email_body = get_acceptance_email(recruitment_name, candidate_name, candidate_email, next_steps)
    
    email = EmailMessage(
        subject=f"Congratulations! Your application for {recruitment_name}",
        body=email_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[candidate_email],
    )
    email.content_subtype = "html"
    email.send()

@login_required
def sendBulkMails(req, id):
  recruitment = get_object_or_404(RecruitmentModel,id= id)
  recruitment.mailSent = True
  recruitment.save()
  appications = CandidateApplicationModel.objects.filter(recruitment = recruitment)
  manager = get_object_or_404(Manager, emailid=req.user.email)
  next_steps = [
                "HR Interview: Our HR team will contact you within 3 working days to schedule your initial interview",
                "Technical Assessment: You'll receive a technical task to complete within 5 days of HR interview",
                "Technical Interview: Upon successful assessment, you'll have a technical discussion with our team",
                "Final Interview: Meeting with department head and key stakeholders",
                "Offer Process: Successful candidates will receive an offer within 2 days of final interview",
                "Onboarding: Selected candidates will begin onboarding the following Monday after acceptance"
            ]
  for app in appications:
     if app.status in ['PENDING','REJECTED']:
        app.status = 'REJECTED'
        
        send_rejection_email(manager.name,app.profile.name, app.profile.email )
     else:
        send_acceptance_email(manager.name,app.profile.name, app.profile.email,next_steps )
     app.save()
  
  return redirect("manager:getApplication",id=id)

@login_required
def manager_dashboard(request):
    candiadtes = CandidateApplicationModel.objects.filter(status='ACCEPTED')
    employees = EmployeeModel.objects.all()
    print(employees, candiadtes)
    non_selected_candidates = []
    emails = set()
    for employee in employees:
       emails.add(employee.profile.email)

    for candidate in candiadtes:
       if candidate.profile.email not in emails:
          non_selected_candidates.append(candidate)

    print(non_selected_candidates)
    return render(request, 'manager/ManagerDashboard.html', {
       'employees' : employees,
       'candidates' : non_selected_candidates
    })

@login_required
def create_employee(req):
        print(" in try ")
        manager = get_object_or_404(Manager, emailid=req.user.email)
        print("manager found", manager)
        if req.method == 'POST':
            print("in post ", req.POST)
            form = EmployeeForm(req.POST)
            # print("form is found ", form)
            if form.is_valid():
                print("form is vaild")
                pro_id = req.GET.get('candidate_id')
                print("id get", pro_id)
                candidate = get_object_or_404(Profile, id=pro_id)
                print("candidate gate", candidate)
                newEmployee = EmployeeModel(
                    experience=form.cleaned_data['experience'],
                    role=form.cleaned_data['role'],
                    manager=manager,
                    employee_type=form.cleaned_data['employee_type'],
                    salary_lpa=form.cleaned_data['salary_lpa'],
                    profile=candidate
                )
                print(newEmployee)
                newEmployee.save()
                
                
            
            # If form is invalid
        return redirect("manager:manager_dashboard")

@login_required
def update_employee(request):
  id=request.GET.get('id')
  employee = get_object_or_404(EmployeeModel, pk=id)
    
  if request.method == 'POST':
      form = EmployeeForm(request.POST, instance=employee)
      print("form is ", form)
      if form.is_valid():
          print("form is valid")
          employee.experience = form.cleaned_data['experience']
          employee.employee_type = form.cleaned_data['employee_type']
          employee.salary_lpa = form.cleaned_data['salary_lpa']
          employee.role = form.cleaned_data['role']
          employee.save()
  return redirect('manager:manager_dashboard')
   
@login_required
def delete_employee(request):
    id=request.GET.get('id')
    employee = get_object_or_404(EmployeeModel, id=id)
    
    if request.method == 'POST':
        employee.delete()
    return redirect('manager:manager_dashboard')

@login_required
def team_management(req):
   teams = TeamModel.objects.all()
   emps = EmployeeModel.objects.all()
   return render(req, "manager/TeamDashboard.html",{
      'teams' : teams,
      'employees' : emps
   })

@login_required
def create_team(req):
    if req.method == 'POST':
        try:
           
            project_name = req.POST.get('project_name')
            description = req.POST.get('project_description')
            team_name = req.POST.get('team_name')
            member_emails = req.POST.getlist('members')
            skills = req.POST.get('skills', '').split(',')
            
            new_team = TeamModel.objects.create(
                project_name=project_name,
                project_description=description,
                team_name=team_name,
                
            )
            
            members = EmployeeModel.objects.filter(profile__email__in=member_emails)
            new_team.team_member.set(members)
            
            
            skills = req.POST.get('skills', '').split(',')
            print(skills)
            new_team.skills = skills
            
            new_team.save()
            return redirect("manager:team")
            
        except Exception as e:
            return redirect("manager:team")
    
    return redirect("manager:team")

@login_required
def team_delete(req,id):
    team = TeamModel.objects.get(id = id)
    team.delete()
    return redirect('manager:team')

@login_required
def team_update(req,id):
	team = TeamModel.objects.get(id=id)
	
  
	if req.method == 'POST':
		form = TeamForm(req.POST,instance=team)
		print('got form to update')
		if form.is_valid():
			team.team_member = form.cleaned_data['team_member']
			team.team_name = form.cleaned_data['team_name']
			team.skills = form.cleaned_data['skills']
			team.project_status = form.cleaned_data['project_status']
			team.project_name = form.cleaned_data['project_name']
			team.project_description = form.cleaned_data['project_description']
			team.save()
			return redirect('manager:team')
	form = TeamForm()
	return render(req,'manager/update_team.html',{'form':form})

@login_required
def toggle_project_status(req,id):
	team = TeamModel.objects.get(id = id)
	team.project_status = 'CP' if team.project_status == 'IP' else 'IP'
	team.save()
	return redirect('manager:team')       

@login_required
def update_team(req, id):
  team = get_object_or_404(TeamModel, id=id)
  if(req.method == 'POST'):
    form = TeamForm(req.POST)
    team.team_member = form.cleaned_data['team_member']
    team.team_name = form.cleaned_data['team_name']
    team.project_name = form.cleaned_data['project_name']
    team.project_status  = form.cleaned_data['project_status']
    team.skills = form.cleaned_data['skills']
    team.save()
  return redirect("manager:team")
