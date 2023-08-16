from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.http import HttpResponse, HttpResponseRedirect
# from .models import <class_name>

# Create your views here.
def reg(response): 

    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            messages.success(response, f"successfully registered with the name {username}")
            form.save()
            return redirect("..")
        else:
            messages.info(response, "The input data is inappropriate")
            return render(response, 'register/registeration_page.html', {'form': form,})
    else:
        form = UserCreationForm()
    return render(response, "register/registeration_page.html", {"form":form})


def home(response): 
    return render(response, "register/home_page.html", {})
