from django.db import transaction

from feed.models import Feed, FeedBookmark
from user.models import Users


# create 할때는 모델 인스턴스 참조, 필터 or get 할때는 id 참조
@transaction.atomic
def do_bookmark(user_id: int, feed_id: int) -> FeedBookmark:
    Users.objects.filter(id=user_id).get()
    Feed.objects.filter(id=feed_id).get()

    return FeedBookmark.objects.create(user_id_id=user_id, feed_id_id=feed_id)


@transaction.atomic
def undo_bookmark(user_id: int, feed_id: int) -> None:
    FeedBookmark.objects.filter(user_id=user_id, feed_id=feed_id).delete()
