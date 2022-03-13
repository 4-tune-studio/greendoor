from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

from feed.models import Feed, FeedLike
from feed.services.feed_service import (
    create_an_feed,
    delete_an_feed,
    get_an_feed,
    get_feed_list,
)
from feed.services.like_service import do_like
from user.models import Users


class TestFeedService(TestCase):
    def test_you_can_create_an_feed(self) -> None:
        # Given
        user = Users.objects.create(username="test")
        content = "test_content"

        # When
        feed = create_an_feed(user.id, content)

        # Then
        self.assertEqual(feed.content, content)

    def test_you_can_get_an_feed_by_id(self) -> None:
        # Given
        content = "test_content"
        user = Users.objects.create(username="test")
        feed = Feed.objects.create(user_id=user, content=content)

        # When
        result_feed = get_an_feed(0, feed.id)

        # Then
        self.assertEqual(feed.id, result_feed.id)
        self.assertEqual(content, result_feed.content)

    def test_it_should_raise_exception_when_feed_does_not_exist(self) -> None:
        # Given
        invalid_feed_id = 9988

        # Expect
        with self.assertRaises(Feed.DoesNotExist):
            get_an_feed(0, invalid_feed_id)

    def test_get_feed_list_should_prefetch_likes(self) -> None:
        # Given
        user = Users.objects.create(username="test")
        feeds = [Feed.objects.create(content=f"{i}", user_id=user) for i in range(1, 21)]
        do_like(user.id, feeds[-1].id)

        with CaptureQueriesContext(connection) as ctx:
            # When
            with self.assertNumQueries(2):
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
        articles = get_feed_list(invalid_user_id, 0, 10)

        # Then
        self.assertEqual(0, len(articles[1].my_likes))
        self.assertEqual(0, len(articles[0].my_likes))

    # 피드가 삭제되는지 검증(like도 같이)
    def test_you_can_delete_an_feed(self) -> None:
        # Given
        user = Users.objects.create(username="test")
        feed1 = Feed.objects.create(content="feed1", user_id=user)
        like = do_like(user.id, feed1.id)

        # When
        delete_an_feed(feed1.id)

        # Then
        self.assertFalse(Feed.objects.filter(id=feed1.id).exists())
        self.assertFalse(FeedLike.objects.filter(id=like.id).exists())
