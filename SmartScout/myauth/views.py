
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,logout,login

# Create your views here.

def new_register(req):
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req,"Registeration succesful. Please login to continue...")
            return render(req,'login.html')
        messages.error(req,"Invalid details. Please try again...")
    
    form =  UserForm()
    return render(req,'signup.html',{'form' : form})

def verify_login(req):
    if req.method == 'POST':
        form = AuthForm(req,data = req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(username = username,password = password)
            
            if user is not None:
                role = form.cleaned_data.get('role')
                if role != 'employee':
                    authCode = form.cleaned_data.get('authCode')
                    if len(authCode) != 6 or authCode is not user.authCode:
                        messages.warning(req,"Enter valid authCode...")
                        return render(req,'login.html',{'form':form})
                
                messages.success(req,"Welcome to SmartScout.")
                login(req,user)
            
            messages.error(req,'User does not exist. Please enter valid data or sign up if not exist.')
            return render(req,'login.html',{'form':form})
        
        messages.error(req,'Enter valid form details...')
        return render(req,'login.html',{'form':form})    
                
    form = AuthForm()
    return render(req,'login.html',{'form':form})                
 
                    
                    
def logout_request(req):
    logout(req)
    messages.success(req,'Logged out successfully...')
    return redirect('smartscout:home')

from django.shortcuts import render

# Create your views here.
def user(req):
  user = req.user

  if user.role is 'employee':
    return render(req,'employee:')
  elif user.role is 'manager':
    return render(req,'manger:')
  
  return render(req,'admin:')
