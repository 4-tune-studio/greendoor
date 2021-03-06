from django.db.models import QuerySet

from feed.models import FeedComment


def create_a_comment(user_id: int, feed_id: int, content: str) -> FeedComment:
    return FeedComment.objects.create(user_id_id=user_id, feed_id_id=feed_id, content=content)


def get_comment_list(feed_id: int, offset: int, limit: int) -> QuerySet[FeedComment]:
    return FeedComment.objects.filter(feed_id=feed_id).order_by("id")[offset : offset + limit]


def delete_a_comment(user_id: int, comment_id: int) -> None:
    FeedComment.objects.filter(id=comment_id, user_id=user_id).delete()


def update_a_comment(user_id: int, comment_id: int, content: str) -> int:
    return FeedComment.objects.filter(id=comment_id, user_id=user_id).update(content=content)
