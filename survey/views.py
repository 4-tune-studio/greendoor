from django.shortcuts import render

# Create your views here.

def home(request):
    print("list 모듈 동작!")
    return render(request, "survey/list.html")