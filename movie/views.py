from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    #return HttpResponse("Welcome to home page")
    #return render(request, 'home.html')
    return render(request, 'home.html', {'name': 'Simon Castro Valencia'})

def about(request):
    #return HttpResponse("Welcome to about page")
    return render (request, 'about.html')