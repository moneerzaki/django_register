from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponse, HttpResponseRedirect
# from .models import <class_name>

# Create your views here.
def reg(response): 

    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect("\home")
    else:
        form = UserCreationForm()
    return render(response, "register/registeration_page.html", {"form":form})