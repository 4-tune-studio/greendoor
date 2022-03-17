from django.db import IntegrityError
from django.test import TestCase

from feed.models import Feed, FeedBookmark
from feed.services.bookmark_service import do_bookmark, undo_bookmark
from user.models import Users


class TestBookmarkService(TestCase):
    # 북마크가 정상적으로 되는지 검증
    def test_a_user_can_bookmark_a_feed(self) -> None:
        # Given / user와 feed가 주어지고
        user = Users.objects.create(username="test")
        feed = Feed.objects.create(user_id=user)

        # When / bookmark 객체가 생성됐을 때
        bookmark = do_bookmark(user.id, feed.id)

        # Then / 아래 내용을 검증한다.
        self.assertIsNotNone(bookmark.id)  # db에서 bookmark pk가 발급이 되었다
        self.assertEqual(user.id, bookmark.user_id.id)  # user id가 bookmark의 user id와 같다.
        self.assertEqual(feed.id, bookmark.feed_id.id)  # feed id가 bookmark의 feed id와 같다.

    # 한 유저가 하나의 피드는 한번만 북마크 할 수 있음을 검증
    def test_a_user_can_bookmark_a_feed_only_once(self) -> None:
        # Given
        user = Users.objects.create(username="test")
        feed = Feed.objects.create(user_id=user)

        # Expect / when이랑 then을 같이 쓸 경우 expect
        do_bookmark(user.id, feed.id)
        # 같은 유저 아이디와 피드 아이디로 bookmark를 생성할 경우 IntegrityError 발생
        with self.assertRaises(IntegrityError):
            do_bookmark(user.id, feed.id)

    # 북마크 취소가 정상적으로 되는지 검증
    def test_a_user_can_undo_like(self) -> None:
        # Given
        user = Users.objects.create(username="test")
        feed = Feed.objects.create(user_id=user)
        bookmark = do_bookmark(user.id, feed.id)

        # When
        undo_bookmark(user.id, feed.id)

        # Then
        with self.assertRaises(FeedBookmark.DoesNotExist):
            FeedBookmark.objects.get(id=bookmark.id)
