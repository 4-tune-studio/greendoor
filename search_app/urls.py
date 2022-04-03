from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('feed_searchResult/', views.feed_searchResult, name='feed_searchResult'),
    path('product_searchResult/', views.product_searchResult, name='product_searchResult'),
]