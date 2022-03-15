from django.urls import path

from . import views

app_name = "feed"

urlpatterns = [
    path("", views.community_view, name="community"),
    path("feed/<int:feed_id>", views.feed_view, name="feed"),
    path("feed/create", views.create_feed_view, name="create_feed"),
    path("api/do_like/<int:feed_id>", views.api_do_like, name="do_like"),
    path("api/undo_like/<int:feed_id>", views.api_undo_like, name="undo_like"),
]
