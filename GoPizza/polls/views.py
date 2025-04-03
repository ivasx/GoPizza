from django.shortcuts import render
from polls.models import Question


# Create your views here.
def question_list(request):
    objects = Question.objects.all()
    context = {'objects': objects}
    return render(request, 'question_list.html', context)