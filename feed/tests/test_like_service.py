from django.db import IntegrityError
from django.test import TestCase

from feed.models import Feed, FeedLike
from feed.services.like_service import do_like, undo_like
from user.models import Users


class TestLikeService(TestCase):
    # 좋아요가 정상적으로 되는지 검증
    def test_a_user_can_like_a_feed(self) -> None:
        # Given / user와 feed가 주어지고
        user = Users.objects.create(username="test")
        feed = Feed.objects.create(user_id=user)

        # When / like 객체가 생성됐을 때
        like = do_like(user.id, feed.id)

        # Then / 아래 내용을 검증한다.
        self.assertIsNotNone(like.id)  # db에서 like pk가 발급이 되었다
        self.assertEqual(user.id, like.user_id.id)  # user id가 like의 user id와 같다.
        self.assertEqual(feed.id, like.feed_id.id)  # feed id가 like의 feed id와 같다.

    # 한 유저가 하나의 피드는 한번만 좋아요 할 수 있음을 검증
    def test_a_user_can_like_a_feed_only_once(self) -> None:
        # Given
        user = Users.objects.create(username="test")
        feed = Feed.objects.create(user_id=user)

        # Expect / when이랑 then을 같이 쓸 경우 expect
        do_like(user.id, feed.id)
        # 같은 유저 아이디와 피드 아이디로 like를 생성할 경우 IntegrityError 발생
        with self.assertRaises(IntegrityError):
            do_like(user.id, feed.id)

    # 좋아요를 할 경우 like_count가 정상적으로 증가하는지 검증
    def test_like_count_should_increase(self) -> None:
        # Given
        user = Users.objects.create(username="test")
        feed = Feed.objects.create(user_id=user)

        # When
        do_like(user.id, feed.id)

        # Then
        # 피드의 좋아요 생성 하나 했을 때 피드의 좋아요 갯수가 1이 맞는지 확인
        feed = Feed.objects.get(id=feed.id)
        self.assertEqual(1, feed.like_count)

    # 좋아요 취소가 정상적으로 되는지 검증
    def test_a_user_can_undo_like(self) -> None:
        # Given
        user = Users.objects.create(username="test")
        feed = Feed.objects.create(user_id=user)
        like = do_like(user.id, feed.id)

        # When
        undo_like(user.id, feed.id)

        # Then
        with self.assertRaises(FeedLike.DoesNotExist):
            FeedLike.objects.get(id=like.id)
