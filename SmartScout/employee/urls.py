
"""
URL configuration for smartscout project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import home, getForm, getJobs, updateProfile, upload_resume

app_name = 'employee'

urlpatterns = [
    path('',home,name="home"),
    path('create/', getForm, name="createCandidate"),
    path('jobs/', getJobs, name="jobs"),
    path('update/<int:id>/', updateProfile, name="updateProfile"),
    path("scanpdf/" ,upload_resume, name="upload_resume")
    
]
