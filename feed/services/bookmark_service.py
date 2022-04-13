from django.db import transaction

from feed.models import FeedBookmark


@transaction.atomic
def do_bookmark(user_id: int, feed_id: int) -> FeedBookmark:
    return FeedBookmark.objects.create(user_id_id=user_id, feed_id_id=feed_id)


@transaction.atomic
def undo_bookmark(user_id: int, feed_id: int) -> None:
    FeedBookmark.objects.filter(user_id=user_id, feed_id=feed_id).delete()
