import json
from datetime import datetime

from django.core import serializers
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from config.utils import allowed_file, get_file_extension
from feed.services.bookmark_service import do_bookmark, undo_bookmark
from feed.services.comment_service import (
    create_a_comment,
    delete_a_comment,
    get_comment_list,
    update_a_comment,
)
from feed.services.feed_service import (
    create_a_feed,
    delete_a_feed,
    get_a_feed,
    get_feed_list,
    get_popular_feed_list,
    increase_views_when_get_a_feed,
    update_a_feed,
    upload_feed_image,
)
from feed.services.like_service import do_like, undo_like
from user.models import UsersFav

URL_LOGIN = "user:sign-in"
URL_COMMUNITY = "feed:community"
URL_FEED = "feed:feed"


def community_view(request: HttpRequest) -> HttpResponse:
    # 요청하는 방식이 get 방식인지 확인
    if request.method == "GET":
        # 로그인이 되어있다면
        if request.user.is_authenticated:
            user_id = request.user.id
            # 설문 조사를 하지 않았다면 설문조사 페이지로 이동
            fav = UsersFav.objects.filter(user_id_id=user_id)
            if len(fav) == 0:
                return redirect("survey:survey")

        # 로그인이 되어있지 않다면
        else:
            # 없는 사용자 id
            user_id = 0

        # 클라이언트에서 전해준 page 값을 저장 (default : none -> 1, "" -> 1)
        page = int(request.GET.get("page", 1) or 1)
        limit = 18
        offset = limit * (page - 1)

        # 피드 리스트 가져오기
        all_feed = get_feed_list(user_id, offset, limit)

        # 첫 페이지라면
        if offset == 0:
            popular_feeds = get_popular_feed_list(user_id, offset, 6)
            return render(request, "index.html", {"all_feed": all_feed, "popular_feeds": popular_feeds})

        # 비동기식
        # offset이 0이 아닐경우 // ajax로 2가 넘어오면 1
        data = serializers.serialize("json", list(all_feed))
        return HttpResponse(json.dumps(data), content_type="application/json")

    # 다른 방식으로 요청이 오면 index 페이지로 리다이렉트
    else:
        return redirect(URL_COMMUNITY)


# 피드를 보여주는 함수
def feed_view(request: HttpRequest, feed_id: int) -> HttpResponse:
    # 요청 방식이 get 방식인지 확인
    if request.method == "GET":
        # 로그인이 되어있다면
        if request.user.is_authenticated:
            # 로그인된 사용자 id
            user_id = request.user.id
        # 로그인이 되어있지 않다면
        else:
            # 없는 사용자 id
            user_id = 0

        # 조회수 1증가시키고 피드 가져오기
        increase_views_when_get_a_feed(feed_id=feed_id)
        feed = get_a_feed(user_id, feed_id)
        comments = get_comment_list(feed.id, 0, 20)  # TODO 코멘트 몇개씩 보이게 할지 정해야함

        return render(request, "feeddetail.html", {"feed": feed, "comments": comments})

    # 다른 방식으로 요청이 오면 index 페이지로 리다이렉트
    else:
        return redirect(URL_COMMUNITY)


# 피드 작성 페이지 뷰, api
def create_feed_view(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect(URL_LOGIN)
    # get 방식일 때
    if request.method == "GET":
        return render(request, "feedwrite.html")
    # post 방식일 때
    elif request.method == "POST":
        # title, content 정보 가져오기
        title = request.POST.get("feed_title", "")
        content = request.POST.get("feed_content", "")
        # title 값이 공백이면
        if title == "":
            return render(request, "feedwrite.html", {"error": "피드에 제목은 필수! :)"})

        # request에 파일 정보가 있으면
        if "feed_img_file" in request.FILES:
            # 사용자 정보 가져오기
            user = request.user
            # request에 있는 file 정보 가져오기
            img_file = request.FILES["feed_img_file"]
            # 파일의 확장자 검사 및 이름을 현재 시간으로 지정
            if img_file and allowed_file(img_file.name):
                ext = get_file_extension(img_file.name)
                filename = f"file_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
                img_file.name = filename
                # 이미지 업로드
                img_url = upload_feed_image(img_file)  # ?를 기준으로 split한 앞쪽 url주소 반환

                # 모든 예외처리를 통과하면
                # 피드 저장 후 저장된 피드의 페이지로 이동
                feed = create_a_feed(user_id=user.id, title=title, image=img_url, content=content)
                return redirect(URL_FEED, feed.id)
            # 허용되지 않은 확장자인 경우
            else:
                return render(request, "feedwrite.html", {"error": "jpg, jpeg, gif, png 확장자를 사용해주세요 :)"})
        # request에 파일 정보가 없으면
        else:
            return render(request, "feedwrite.html", {"error": "피드에 사진은 필수! :)"})
    # 그 외 방식일 때
    else:
        return redirect(URL_COMMUNITY)


# 피드 업데이트 함수
def update_feed_view(request: HttpRequest, feed_id: int) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect(URL_LOGIN)
    user_id = request.user.id
    feed = get_a_feed(user_id=user_id, feed_id=feed_id)

    # GET 방식일 때
    if request.method == "GET":
        if user_id == feed.user_id.id:
            return render(request, "feedmodify.html", {"feed": feed})
        # 피드 작성자가 아닌 다른 유저가 유청할 때
        else:
            return redirect(URL_COMMUNITY)

    # POST 방식일 때
    elif request.method == "POST":
        # title, content 정보 가져오기
        title = request.POST.get("feed_title", "")
        content = request.POST.get("feed_content", "")

        # request에 파일 정보가 있으면
        if "feed_img_file" in request.FILES:
            # request에 있는 file 정보 가져오기
            img_file = request.FILES["feed_img_file"]
            # 파일의 확장자 검사 및 이름을 현재 시간으로 지정
            if img_file and allowed_file(img_file.name):
                ext = get_file_extension(img_file.name)
                filename = f"file_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
                img_file.name = filename
                # 이미지 업로드
                img_url = upload_feed_image(img_file)

                # 모든 예외처리를 통과하면
                # 피드 업데이트 후 저장된 피드의 페이지로 이동
                update_a_feed(user_id=user_id, feed_id=feed_id, title=title, image=img_url, content=content)
                return redirect(URL_FEED, feed_id)
            # 허용되지 않은 확장자인 경우
            else:
                return render(
                    request,
                    "feedmodify.html",
                    {"feed": feed, "error": "jpg, jpeg, gif, png 확장자를 사용해주세요 :)"},
                )
        # request에 파일 정보가 없으면 기존 이미지 사용
        else:
            # 피드 업데이트 후 저장된 피드의 페이지로 이동
            update_a_feed(user_id=user_id, feed_id=feed_id, title=title, image=feed.image, content=content)
            return redirect(URL_FEED, feed_id)

    # POST와 GET 이외의 요청일 때
    else:
        return redirect(URL_COMMUNITY)


# 피드 삭제 api
def api_delete_feed(request: HttpRequest, feed_id: int) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect(URL_LOGIN)
    user_id = request.user.id
    # 피드 삭제 서비스 함수 실행
    delete_a_feed(feed_id=feed_id, user_id=user_id)
    return redirect(URL_COMMUNITY)


# 좋아요 api
@require_POST
def api_like(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect(URL_LOGIN)

    # 사용자 정보 가져오기
    user = request.user
    feed_id = int(request.POST["feed_id"])
    feed = get_a_feed(user_id=user.id, feed_id=feed_id)
    feed_like_count = feed.like_count

    # 좋아요를 한 상태이면 좋아요 취소
    if feed.my_likes:
        undo_like(user_id=user.id, feed_id=feed_id)
        msg = "좋아요 취소"
        feed_like_count -= 1
    # 좋아요를 안한 상태이면 좋아요
    else:
        do_like(user_id=user.id, feed_id=feed_id)
        msg = "좋아요"
        feed_like_count += 1

    # 프론트에 보낼 정보를 json타입으로 만들어주기
    context = {"msg": msg, "like_count": feed_like_count}
    return HttpResponse(json.dumps(context), content_type="application/json")


# 북마크 api
@require_POST
def api_bookmark(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect(URL_LOGIN)

    # 사용자 정보 가져오기
    try:
        user = request.user
        feed_id = int(request.POST["feed_id"])
    except Exception as e:
        print(e)
    feed = get_a_feed(user_id=user.id, feed_id=feed_id)
    # 북마크를 한 상태이면 북마크 취소
    if feed.my_bookmark:
        undo_bookmark(user_id=user.id, feed_id=feed_id)
        msg = "북마크 취소"
    # 북마크를 안한 상태이면 북마크
    else:
        do_bookmark(user_id=user.id, feed_id=feed_id)
        msg = "북마크"

    # 프론트에 보낼 정보를 json타입으로 만들어주기
    context = {"msg": msg}
    return HttpResponse(json.dumps(context), content_type="application/json")


# 댓글 작성 api
@require_POST
def api_create_comment(request: HttpRequest, feed_id: int) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect(URL_LOGIN)

    # 사용자 정보 가져오기
    user = request.user
    # post 형식의 form 태그에서 content를 가져옴
    content = request.POST.get("comment_content", "")
    # 댓글 생성 서비스 함수 실행
    create_a_comment(user_id=user.id, feed_id=feed_id, content=content)
    return redirect(URL_FEED, feed_id)


# 댓글 수정
@require_POST
def api_update_comment(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect(URL_LOGIN)

    user_id = request.user.id
    # request에 담긴 정보를 가져옴
    comment_id = int(request.POST["comment_id"])
    content = request.POST["content"]
    update_a_comment(user_id=user_id, comment_id=comment_id, content=content)
    # 프론트에 보낼 정보를 json타입으로 만들어주기
    context = {"msg": "success"}
    return HttpResponse(json.dumps(context), content_type="application/json")


# 댓글 삭제 api
def api_delete_comment(request: HttpRequest, feed_id: int, comment_id: int) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect(URL_LOGIN)

    user_id = request.user.id
    # 댓글 삭제 서비스 함수 실행
    delete_a_comment(comment_id=comment_id, user_id=user_id)
    return redirect(URL_FEED, feed_id)
