from django.db import transaction
from django.db.models import F

from feed.models import Feed, FeedLike
from user.models import Users


# create 할때는 모델 인스턴스 참조, 필터 or get 할때는 id 참조
@transaction.atomic
def do_like(user_id: int, feed_id: int) -> FeedLike:
    # Users.objects.filter(id=user_id).get()
    # feed = Feed.objects.filter(id=feed_id).get()

    Feed.objects.filter(id=feed_id).update(like_count=F("like_count") + 1)
    like = FeedLike.objects.create(user_id_id=user_id, feed_id_id=feed_id)

    return like


@transaction.atomic
def undo_like(user_id: int, feed_id: int) -> None:
    deleted_cnt, _ = FeedLike.objects.filter(user_id=user_id, feed_id=feed_id).delete()
    if deleted_cnt:
        Feed.objects.filter(id=feed_id).update(like_count=F("like_count") - 1)
