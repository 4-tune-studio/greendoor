from typing import Any, List

from django.db import models

from config.models import BaseModel
from user.models import Users


class Feed(BaseModel):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="feed", db_column="user_id")
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=256)
    content = models.CharField(max_length=500, blank=True, null=True)
    like_count = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    my_likes: List[Any]  # Prefetch 에서 사용용
    my_bookmark: List[Any]  # Prefetch 에서 사용용


class FeedComment(BaseModel):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="feed_comment", db_column="user_id")
    feed_id = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="feed_comment", db_column="feed_id")
    content = models.CharField(max_length=200)


class FeedLike(BaseModel):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="feed_like", db_column="user_id")
    feed_id = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="feed_like", db_column="feed_id")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user_id", "feed_id"], name="unique_user_feedlike"),
        ]


class FeedBookmark(BaseModel):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="feed_bookmark", db_column="user_id")
    feed_id = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="feed_bookmark", db_column="feed_id")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user_id", "feed_id"], name="unique_user_feedbookmark"),
        ]


class Img(BaseModel):
    img = models.ImageField(upload_to="feed/%Y%m%d", max_length=255)
