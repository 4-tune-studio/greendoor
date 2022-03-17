from django.test import TestCase

from feed.models import Feed, FeedComment
from feed.services.comment_service import (
    create_a_comment,
    delete_a_comment,
    get_comment_list,
    update_a_comment,
)
from user.models import Users


class TestCommentService(TestCase):
    # 코멘트가 정상적으로 만들어지는지 검증
    def test_you_can_create_a_comment(self) -> None:
        # Given
        user = Users.objects.create(username="test")
        feed = Feed.objects.create(user_id=user)
        content = "comment"

        # When
        comment = create_a_comment(user.id, feed.id, content)

        # Then
        self.assertEqual(comment.content, content)  # 만들어진 코멘트의 컨텐츠와 주어진 컨텐츠가 일치하는지 확인

    # comment 리스트를 정상적으로 가져오는지 검증
    def test_get_comment_list(self) -> None:
        # Given
        user = Users.objects.create(username="test")
        feed = Feed.objects.create(user_id=user)
        comments = [FeedComment.objects.create(content=f"#{i}", user_id=user, feed_id=feed) for i in range(1, 21)]

        # When
        with self.assertNumQueries(1):
            result_comments = get_comment_list(feed.id, 0, 10)

            # Then
            # 가져온 comment 리스트가 10 과 일치하는지
            self.assertEqual(len(result_comments), 10)
            # 만든 comment의 최신순 10개와 가져온 피드 10개의 아이디가 각각 일치하는지
            self.assertEqual([a.id for a in (comments[0:10])], [a.id for a in result_comments])

    # comment가 삭제되는지 검증
    def test_you_can_delete_a_comment(self) -> None:
        # Given
        user = Users.objects.create(username="test")
        feed = Feed.objects.create(user_id=user)
        content = "test comment"
        comment = create_a_comment(user.id, feed.id, content)

        # When
        delete_a_comment(comment_id=comment.id, user_id=user.id)

        # Then
        self.assertFalse(FeedComment.objects.filter(id=comment.id).exists())

    # comment가 수정되는지 검증
    def test_you_can_update_a_comment(self) -> None:
        # Given
        user = Users.objects.create(username="test")
        feed = Feed.objects.create(user_id=user)
        content1 = "test comment"
        comment = create_a_comment(user.id, feed.id, content1)
        content2 = "update test comment"

        # When
        update_a_comment(comment_id=comment.id, user_id=user.id, content=content2)
        result = FeedComment.objects.get(id=comment.id)

        # Then
        self.assertEqual(result.content, content2)  # 수정된 코멘트의 컨텐츠와 주어진 컨텐츠가 일치하는지 확인
