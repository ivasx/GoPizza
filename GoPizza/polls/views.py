from django.shortcuts import render, redirect
from polls.forms import RegistrationForm
from polls.models import Question
from django.contrib.auth.forms import *
from django import forms
from django.contrib.auth import login, logout, authenticate
from .forms import UserLoginForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home_view(request):
    return render(request, 'home.html')

# View for question list (login required)
@login_required
def question_list(request):
    objects = Question.objects.all()
    context = {'questions': objects}
    return render(request, 'question_list.html', context)

# Registration view
def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('polls:question_list')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {"form": form})

# Login view
def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('polls:question_list')  # Перехід на список запитань після входу
    else:
        form = UserLoginForm()

    return render(request, 'polls/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('polls:login')
