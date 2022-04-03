from django.shortcuts import render, redirect

from user.models import UsersFav
from .models import Question


URL_LOGIN = "user:sign-in"
URL_COMMUNITY = "feed:community"
URL_SURVEY = "feed:community"


# Create your views here.

def survey(request):
    if not request.user.is_authenticated:
        return redirect(URL_LOGIN)

    user = request.user
    if request.method == "POST":
        result1 = request.POST.get("survey=1", None)
        result2 = request.POST.get("survey=2", None)
        result3 = request.POST.get("survey=3", None)

        if result1 == None or result2 == None or result3 == None:
            return redirect(URL_SURVEY)

        UsersFav.objects.create(user_id=user, result1=result1, result2=result2, result3=result3)
        return redirect(URL_COMMUNITY)

    else:
        questions = Question.objects.all()

        context = {
            "questions": questions,
        }

        return render(request, "survey/survey.html", context=context)

