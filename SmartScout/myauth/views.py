
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,logout,login

from .forms import UserForm,AuthForm
import os
# Create your views here.

def new_register(req):
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            newUser =  form.save(commit=False)
            newUser.role = "employee"
            form.save()
            messages.success(req,"Registeration succesful. Please login to continue...")
            return redirect('/myauth/login')
        messages.error(req,"Invalid details. Please try again...")
        return render(req, 'myauth/register.html', {'form': form})
    
    form =  UserForm()
    return render(req,'myauth/register.html',{'form' : form})


def verify_login(req):
    if req.method == 'POST':
        form = AuthForm(req, data=req.POST)
        print("Form received:", req.POST)
        
        if form.is_valid():
            print("Form is valid!") 
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print("Authenticated User:", user) 
            
            if user is not None:
                role = form.cleaned_data.get('role')
                print("User role:", role) 

                
                if role != 'employee':
                    if role == 'manager':
                  
                        login(req, user)
                        return redirect('/manager')
                    else:
                        
                        login(req, user)
                        print("in bro")
                        return redirect('/myadmin/') 
                        

                messages.success(req, "Welcome to SmartScout.")
                print(user)
                login(req, user)
                print("User logged in successfully!")  
                return redirect('/employee') 

            messages.error(req, 'User does not exist. Please enter valid data or sign up if not exist.')
        else:
            print("Form Errors:", form.errors)  
            messages.error(req, 'Enter valid form details...')

        return render(req, 'myauth/login.html', {'form': form,'errors': form.errors})  

    form = AuthForm()
    return render(req, 'myauth/login.html', {'form': form})
   
   
               
def logout_request(req):
    logout(req)
    messages.success(req,'Logged out successfully...')
    return redirect('home')

from django.shortcuts import render

# Create your views here.
def user(req):
  user = req.user

  if user.role is 'employee':
    return render(req,'employee:')
  elif user.role is 'manager':
    return render(req,'manger:')
  
  return render(req,'admin:')
