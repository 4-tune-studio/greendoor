from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

from feed.models import Feed, FeedLike
from feed.services.feed_service import (
    create_a_feed,
    delete_a_feed,
    get_a_feed,
    get_feed_list,
    update_a_feed,
)
from feed.services.like_service import do_like
from user.models import Users


class TestFeedService(TestCase):
    def test_you_can_create_a_feed(self) -> None:
        # Given
        user = Users.objects.create(username="test")
        title = "test_feed"
        image = "https://test/image/url"
        content = "test_content"

        # When
        feed = create_a_feed(user_id=user.id, title=title, image=image, content=content)

        # Then
        self.assertEqual(feed.user_id_id, user.id)
        self.assertEqual(feed.title, title)
        self.assertEqual(feed.image, image)
        self.assertEqual(feed.content, content)

    def test_you_can_get_a_feed_by_id(self) -> None:
        # Given
        content = "test_content"
        user = Users.objects.create(username="test")
        feed = Feed.objects.create(user_id=user, content=content)

        # When
        result_feed = get_a_feed(0, feed.id)

        # Then
        self.assertEqual(feed.id, result_feed.id)
        self.assertEqual(content, result_feed.content)

    def test_it_should_raise_exception_when_feed_does_not_exist(self) -> None:
        # Given
        invalid_feed_id = 9988

        # Expect
        with self.assertRaises(Feed.DoesNotExist):
            get_a_feed(0, invalid_feed_id)

    def test_get_feed_list_should_prefetch_likes(self) -> None:
        # Given
        user = Users.objects.create(username="test")
        feeds = [Feed.objects.create(content=f"{i}", user_id=user) for i in range(1, 21)]
        do_like(user.id, feeds[-1].id)

        with CaptureQueriesContext(connection) as ctx:
            # When
            with self.assertNumQueries(3):
                result_feeds = get_feed_list(user.id, 0, 10)
                result_counts = [a.like_count for a in result_feeds]

                # Then
                # 가져온 피드 리스트가 10 과 일치하는지
                self.assertEqual(len(result_feeds), 10)
                # 가장 최신 피드의 좋아요 개수가 1인지
                self.assertEqual(1, result_counts[0])
                # 만든 피드의 최신순 10개와 가져온 피드 10개의 아이디가 각각 일치하는지
                self.assertEqual([a.id for a in reversed(feeds[10:21])], [a.id for a in result_feeds])

    def test_get_feed_list_should_contain_my_likes_when_like_exists(self) -> None:
        # Given
        user = Users.objects.create(username="test")
        feed1 = Feed.objects.create(content="feed1", user_id=user)
        like = do_like(user.id, feed1.id)
        Feed.objects.create(content="feed2", user_id=user)

        # When
        feeds = get_feed_list(user.id, 0, 10)

        # Then
        self.assertEqual(like.id, feeds[1].my_likes[0].id)
        self.assertEqual(0, len(feeds[0].my_likes))

    # 유저 아이디가 없는 아이디일 경우 my_likes가 전부 비어있는지 검사
    def test_get_feed_list_should_not_contain_my_likes_when_user_id_is_zero(
        self,
    ) -> None:
        # Given
        user = Users.objects.create(username="test")
        feed1 = Feed.objects.create(content="feed1", user_id=user)
        FeedLike.objects.create(user_id_id=user.id, feed_id_id=feed1.id)
        Feed.objects.create(content="feed2", user_id=user)
        invalid_user_id = 0

        # When
        feeds = get_feed_list(invalid_user_id, 0, 10)

        # Then
        self.assertEqual(0, len(feeds[1].my_likes))
        self.assertEqual(0, len(feeds[0].my_likes))

    # 피드가 삭제되는지 검증(like도 같이)
    def test_you_can_delete_a_feed(self) -> None:
        # Given
        user = Users.objects.create(username="test")
        feed1 = Feed.objects.create(content="feed1", user_id=user)
        like = do_like(user.id, feed1.id)

        # When
        delete_a_feed(feed_id=feed1.id, user_id=user.id)

        # Then
        self.assertFalse(Feed.objects.filter(id=feed1.id).exists())
        self.assertFalse(FeedLike.objects.filter(id=like.id).exists())

    # feed가 수정되는지 검증
    def test_you_can_update_a_feed(self) -> None:
        # Given
        user = Users.objects.create(username="test")
        title1 = "test feed"
        image1 = "https://test.jpg"
        content1 = "test feed"

        feed = Feed.objects.create(user_id=user, title=title1, image=image1, content=content1)
        title2 = "test2 feed"
        image2 = "https://image2.jpg"
        content2 = "update test feed"

        # When
        update_a_feed(user_id=user.id, feed_id=feed.id, title=title2, image=image2, content=content2)
        result = Feed.objects.get(id=feed.id)

        # Then
        self.assertEqual(result.title, title2)  # 수정된 피드의 title이 주어진 title2와 일치하는지 확인
        self.assertEqual(result.image, image2)  # 수정된 피드의 이미지와 주어진 이미지가 일치하는지 확인
        self.assertEqual(result.content, content2)  # 수정된 피드의 컨텐츠와 주어진 컨텐츠가 일치하는지 확인
