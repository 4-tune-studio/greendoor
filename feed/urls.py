from django.urls import path

from . import views

app_name = "feed"

urlpatterns = [
    path("", views.community_view, name="community"),
    path("feed/<int:feed_id>", views.feed_view, name="feed"),
    path("feed/create", views.create_feed_view, name="create_feed"),
    path("api/delete_feed/<int:feed_id>", views.api_delete_feed, name="delete_feed"),
    path("api/do_like/<int:feed_id>", views.api_do_like, name="do_like"),
    path("api/undo_like/<int:feed_id>", views.api_undo_like, name="undo_like"),
    path("api/do_bookmark/<int:feed_id>", views.api_do_bookmark, name="do_bookmark"),
    path("api/undo_bookmark/<int:feed_id>", views.api_undo_bookmark, name="undo_bookmark"),
    path("api/create_comment/<int:feed_id>", views.api_create_comment, name="create_comment"),
    path("api/delete_comment/<int:feed_id><int:comment_id>", views.api_delete_comment, name="delete_comment"),
]
