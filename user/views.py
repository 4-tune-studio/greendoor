from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse

from django.shortcuts import redirect, render

from user.forms import CustomUserChangeForm
from user.models import Users

# Create your views here.

# =============== 장고 인증 URL + 템플릿 연결 함수 ================ #
# def accounts_login(request):
#     if request.method == 'GET':
#         return render(request, 'user/signin.html')


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

    else:
        return redirect("/")


def logout(request: HttpRequest) -> HttpResponse:
    auth.logout(request)  # 인증 되어있는 정보를 없애기
    return redirect("/")


# user 프로필 update
@login_required(login_url="signin")
def edit(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.nickname = request.POST["nickname"]
            form.zipcode = request.POST["zipcode"]
            form.address = request.POST["address"]
            form.phonenumber = request.POST["phonenumber"]
            form.save()
            return redirect("/")
    # method == 'GET' 일 때
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {"form": form}
    # 관련 templates 기존 정보를 넘겨 준다
    return render(request, "user_test/edit.html", context)  # TODO 템플릿 변경시 경로 변경하기



# user profile update 페이지 /password_reset/ url 연결
def password(request: HttpRequest) -> HttpResponse:
    return redirect("/password_reset/")


@require_POST
def api_update_user_image(request):
    return 0
