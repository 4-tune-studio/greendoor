from django.contrib.auth import views as auth_views
from django.urls import include, path
from survey import views



app_name = "survey"

urlpatterns=[
    path('sign-up/survey', views.home),
]