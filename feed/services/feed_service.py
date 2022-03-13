from django.db.models import Prefetch, QuerySet

from feed.models import Feed, FeedLike


def create_an_feed(user_id: int, content: str) -> Feed:
    return Feed.objects.create(user_id_id=user_id, content=content)


def get_an_feed(user_id: int, article_id: int) -> Feed:
    return Feed.objects.prefetch_related(
        Prefetch(
            "feed_like",
            queryset=FeedLike.objects.filter(user_id=user_id),
            to_attr="my_likes",
        )
    ).get(id=article_id)


# prefetch_related를 통해 lazy한 작업을 미리 처리 (관계된 데이터를 미리 가져오기)
# Prefetch object를 사용해서 prefetch를 할 때 필터링을 하고 조건에 맞는 값을 to_attr를 통해 해당 필드에 set
def get_feed_list(user_id: int, offset: int, limit: int) -> QuerySet[Feed]:
    return Feed.objects.order_by("-id").prefetch_related(
        Prefetch(
            "feed_like",
            queryset=FeedLike.objects.filter(user_id=user_id),
            to_attr="my_likes",
        )
    )[offset : offset + limit]


def delete_an_feed(feed_id: int) -> None:
    Feed.objects.filter(id=feed_id).delete()
