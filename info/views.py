from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from info.models import Info


# Create your views here.
def info_view(request: HttpRequest) -> HttpResponse:
    infos = Info.objects.all()
    return render(request, "info/info.html", {"infos": infos})
