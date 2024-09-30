# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from ecommerceapp.models import *
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            # Log in the user after signup
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')  # Redirect to home page after successful signup
    else:
        form = SignupForm()
    settings = Settings.objects.first()
    context ={
        'form': form,
        'settings':settings,

    }
    return render(request, 'accounts/signup.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                login(request, user)
                return redirect('/admin')  # Redirect to home page after successful login
            elif user.is_staff:
                login(request, user)
                return redirect('/admin')
            else:
                login(request, user)
                return redirect('/')
        messages.add_message(request, messages.SUCCESS, "Successfully Login")
    else:
        form = AuthenticationForm()
    
    settings = Settings.objects.first()
    context ={
        'form': form,
        'settings':settings,

    }
    return render(request, 'accounts/login.html', context)

def logout_view(request):
    if request.method == 'GET':
        logout(request)
        HttpResponse("Success")
        return redirect('/')
    messages.add_message(request, messages.SUCCESS, "Successfully Logout")