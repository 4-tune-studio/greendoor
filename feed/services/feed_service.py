from django.core.files.uploadedfile import UploadedFile
from django.db.models import Prefetch, QuerySet

from feed.models import Feed, FeedBookmark, FeedLike, Img


def upload_feed_image(img_file: UploadedFile) -> Img:
    return Img.objects.create(img=img_file)


def create_an_feed(user_id: int, title: str, image: str, content: str) -> Feed:
    return Feed.objects.create(user_id_id=user_id, title=title, image=image, content=content)


def get_an_feed(user_id: int, feed_id: int) -> Feed:
    return (
        Feed.objects.prefetch_related(
            Prefetch(
                "feed_like",
                queryset=FeedLike.objects.filter(user_id=user_id),
                to_attr="my_likes",
            )
        )
        .prefetch_related(
            Prefetch(
                "feed_bookmark",
                queryset=FeedBookmark.objects.filter(user_id=user_id),
                to_attr="my_bookmark",
            )
        )
        .get(id=feed_id)
    )


# prefetch_related를 통해 lazy한 작업을 미리 처리 (관계된 데이터를 미리 가져오기)
# Prefetch object를 사용해서 prefetch를 할 때 필터링을 하고 조건에 맞는 값을 to_attr를 통해 해당 필드에 set
def get_feed_list(user_id: int, offset: int, limit: int) -> QuerySet[Feed]:
    return (
        Feed.objects.order_by("-id")
        .prefetch_related(
            Prefetch(
                "feed_like",
                queryset=FeedLike.objects.filter(user_id=user_id),
                to_attr="my_likes",
            )
        )
        .prefetch_related(
            Prefetch(
                "feed_bookmark",
                queryset=FeedBookmark.objects.filter(user_id=user_id),
                to_attr="my_bookmark",
            )
        )[offset : offset + limit]
    )


# 좋아요 인기순으로 피드 가져오기
def get_popular_feed_list(user_id: int, offset: int, limit: int) -> QuerySet[Feed]:
    return (
        Feed.objects.order_by("-like_count")
        .prefetch_related(
            Prefetch(
                "feed_like",
                queryset=FeedLike.objects.filter(user_id=user_id),
                to_attr="my_likes",
            )
        )
        .prefetch_related(
            Prefetch(
                "feed_bookmark",
                queryset=FeedBookmark.objects.filter(user_id=user_id),
                to_attr="my_bookmark",
            )
        )[offset : offset + limit]
    )


# 피드 삭제 함수
def delete_an_feed(feed_id: int) -> None:
    Feed.objects.filter(id=feed_id).delete()


# 피드 업데이트(수정) 함수
def update_an_feed(feed_id: int, title: str, image: str, content: str) -> int:
    return Feed.objects.filter(id=feed_id).update(title=title, image=image, content=content)
