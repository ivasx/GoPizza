from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from polls.forms import RegistrationForm
from polls.models import Question
from django.contrib.auth.forms import *


# Create your views here.
def question_list(request):
    objects = Question.objects.all()
    context = {'questions': objects}
    return render(request, 'question_list.html', context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:question_list')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})