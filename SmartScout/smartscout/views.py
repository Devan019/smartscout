

from django.shortcuts import redirect, render

def home(req):
  return  render(req,"home.html")

def notfound(req,exception):
  return render(req, 'include/404.html', status=404)