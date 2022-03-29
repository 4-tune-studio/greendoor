from django.contrib import auth
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from config.utils import allowed_file, get_file_extension
from feed.services.feed_service import get_my_bookmark_feed_list, get_my_feed_list
from user.forms import CustomUserChangeForm
from user.models import Users
from user.services.userimg_service import update_user_image, update_user_image_url

# Create your views here.


def sign_up_view(request: HttpRequest) -> HttpResponse:

    if request.method == "GET":
        user = request.user.is_authenticated  # 로그인 된 사용자가 요청하는지 검사
        if user:  # 로그인이 되어있다면
            return redirect("/")
        else:  # 로그인이 되어있지 않다면
            return render(request, "user/signup.html")
    elif request.method == "POST":
        username = str(request.POST.get("username", None))
        password = request.POST.get("password", None)
        password2 = request.POST.get("password2", None)

        if password != password2:
            return render(request, "user/signup.html")
        else:
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, "user/signup.html")  # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
            else:
                Users.objects.create_user(username=username, password=password)
                return redirect("/sign-in")  # 회원가입이 완료되었으므로 로그인 페이지로 이동
    else:
        return redirect("/")


def sign_in_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)

        me = auth.authenticate(request, username=username, password=password)  # 사용자 불러오기
        if me is not None:  # 저장된 사용자의 패스워드와 입력받은 패스워드 비교
            auth.login(request, me)
            return redirect("/")
        else:
            return redirect("/sign-in")  # 로그인 실패
    elif request.method == "GET":
        user = request.user.is_authenticated  # 사용자가 로그인 되어 있는지 검사
        if user:  # 로그인이 되어 있다면
            return redirect("/")
        else:  # 로그인이 되어 있지 않다면
            return render(request, "user/signin.html")
    else:
        return redirect("/")


def logout(request: HttpRequest) -> HttpResponse:
    auth.logout(request)  # 인증 되어있는 정보를 없애기
    return redirect("/")


# =============== 장고 인증 URL + 템플릿 연결 함수 ================ #
def accounts_login(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "signin.html")  # TODO 템플릿 변경시 경로 변경하기1
    else:
        return redirect("/")


# =============== user profile update (text) ================ #
# user 주소, 번호 update
def profile_edit(request: HttpRequest, pk: int) -> HttpResponse:
    # 사용자 로그인 확인
    if not request.user.is_authenticated:
        return redirect("user/signin.html")  # TODO 템플릿 변경시 경로 변경하기1
    # 다른 사용자 수정 불가
    if request.user.id == pk:
        if request.method == "POST":
            # 추가 아닌 수정. 때문에 기존 정보를 가져오기 위해 instance 지정해 준다.
            form = CustomUserChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                form.bio = request.POST["zipcode"]
                form.image = request.POST["address"]
                form.image = request.POST["phonenumber"]
                form.save()
                return redirect("/")

        elif request.method == "GET":
            form = CustomUserChangeForm(instance=request.user)
        context = {"form": form}
        # 관련 templates 기존 정보를 넘겨 준다
        return render(request, "user_test/edit.html", context)  # TODO 템플릿 변경시 경로 변경하기2
    else:
        return redirect("/")  # TODO 잘못된 접근 경고문 여부


# user profile update 페이지 -> /password_reset/ url 연결
def password(request: HttpRequest) -> HttpResponse:
    return redirect("/password_reset/")


# =============== user profile update (image) ================ #
def api_update_user_image(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect("/")  # TODO 템플릿 변경시 경로 변경하기3
    if request.method == "POST":
        if "image" in request.FILES:
            # json data 변수에 저장
            user_id = request.POST["user_id"]
            img_file = request.FILES["image"]

            # 이미지 파일 이름 -> user id로 변경 // utils.py 함수 사용
            if img_file and allowed_file(img_file.name):
                ext = get_file_extension(img_file.name)
                filename = f"{user_id}.{ext}"
                img_file.name = filename

                # s3 image upload, s3 url - users 모델 저장
                img_update = update_user_image(img_file)

                # Users 'image' 필드에 url update
                url_update = update_user_image_url(user_id, img_update)
                return JsonResponse({"message": url_update})
            else:
                return JsonResponse({"message": "올바른 이미지 확장자가 아닙니다."})


# =============== user my page ================ #
def user_my_page(request: HttpRequest, pk: int) -> HttpResponse:
    # 사용자 로그인 확인
    if not request.user.is_authenticated:
        return redirect("/sign-in/")

    # 다른 사용자 수정 불가
    if request.user.id == pk:
        if request.method == "GET":
            my_feed_list = get_my_feed_list(pk)
            my_bookmark_list = get_my_bookmark_feed_list(pk)
            return render(request, "mypage.html", {"feed_list": my_feed_list, "bookmark_list": my_bookmark_list})
        else:
            return redirect("/")  # TODO 잘못된 접근 경고문 여부

