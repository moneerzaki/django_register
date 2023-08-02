from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
# from django.http import HttpResponse, HttpResponseRedirect

# from .models import <class_name>

# Create your views here.
def homepage(response): 
    return render(response, "project1/homepage.html", {})
    # return render(response, "register/homepage.html", {})

