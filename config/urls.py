"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path("admin/", admin.site.urls),
# ]
from typing import Dict

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import HttpRequest
from django.urls import include, path
from ninja import NinjaAPI

from user import views

api = NinjaAPI()


@api.get("/add")
def add(request: HttpRequest, a: int, b: int) -> Dict[str, int]:
    return {"result": a + b}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("cart/", include("cart.urls")),

    # path("community/", include("feed.urls")),
    path("", include("feed.urls")),
    path("user/", include("user.urls")),
    path("survey/", include("survey.urls")),
    path("order/", include("order.urls")),

    path("product/", include("product.urls")),
    path("google/", include("allauth.urls")),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="password/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(template_name="password/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(template_name="password/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
