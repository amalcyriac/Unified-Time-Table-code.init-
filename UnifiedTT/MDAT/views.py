from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("Hello, world !")

def new_admin(request):
    return render(request,'admin_page.html')
    #return HttpResponse("Welcome to admin page!")

def update_database_dss(request):
    return HttpResponse("File received thankyou!")
