from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("Hello, world !")

def new_admin(request):
    return render(request,'admin.html')
    #return HttpResponse("Welcome to admin page!")
