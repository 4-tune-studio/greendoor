from django.urls import path

from feed import views

app_name = "feed"

urlpatterns = [
    path("", views.community_view, name="community"),
    path("feed/<int:feed_id>", views.feed_view, name="feed"),
    path("feed/create", views.create_feed_view, name="create_feed"),
    path("feed/update/<int:feed_id>", views.update_feed_view, name="update_feed"),
    path("api/delete_feed/<int:feed_id>", views.api_delete_feed, name="delete_feed"),
    path("api/api_like", views.api_like, name="api_like"),
    path("api/api_bookmark", views.api_bookmark, name="api_bookmark"),
    path("api/create_comment/<int:feed_id>", views.api_create_comment, name="create_comment"),
    path("api/update_comment", views.api_update_comment, name="update_comment"),
    path("api/delete_comment/<int:feed_id>/<int:comment_id>", views.api_delete_comment, name="delete_comment"),
]
