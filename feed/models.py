from django.db import models

from greendoor.models import BaseModel
from user.models import Users


class Feed(BaseModel):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="feed", db_column="user_id")
    image = models.CharField(max_length=256)
    content = models.CharField(max_length=500, blank=True, null=True)


class FeedComment(BaseModel):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="feed_comment", db_column="user_id")
    feed_id = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="feed_comment", db_column="feed_id")
    content = models.CharField(max_length=200)


class FeedLike(BaseModel):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="feed_like", db_column="user_id")
    feed_id = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="feed_like", db_column="feed_id")
    like = models.IntegerField()


class FeedBookmark(BaseModel):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="feed_bookmark", db_column="user_id")
    feed_id = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="feed_bookmark", db_column="feed_id")
    bookmark = models.IntegerField()
