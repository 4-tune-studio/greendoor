from django.shortcuts import render

from .models import Choice, Level, Question


# Create your views here.
def form(request):
    questions = Question.objects.all()

    context = {
        "questions": questions,
    }

    return render(request, "survey/form.html", context=context)


def result(request):

    return render(request, "survey/result.html")
