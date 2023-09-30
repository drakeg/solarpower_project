# views.py in the solarpower app
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm

logout_view = LogoutView.as_view()

def home(request):
    active_page = 'home'
    return render(request, 'home.html', {'active_page': active_page})

def calculator(request):
    active_page = 'calculator'
    # Add any necessary context data for your calculator page here
    return render(request, 'calculator.html', {'active_page': active_page})

def user_profile(request):
    # Add any necessary context data for the user profile page here
    return render(request, 'user_profile.html', {'user': request.user})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_profile')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')  # Redirect to the home page