# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
# from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, redirect
# from .models import <class_name>
from .models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def homepage(response): 
    context = {
            'posts': Post.objects.all()
        }
    return render(response, "project1/homepage.html", context)
    # return render(response, "register/homepage.html", {})

