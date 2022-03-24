from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from user.forms import CustomUserChangeForm

# Create your views here.

# =============== 장고 인증 URL + 템플릿 연결 함수 ================ #
# def accounts_login(request):
#     if request.method == 'GET':
#         return render(request, 'user/signin.html')


# user 프로필 update
@login_required(login_url="signin")
def edit(request, pk):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.email = request.POST["nickname"]
            form.bio = request.POST["zipcode"]
            form.image = request.POST["address"]
            form.image = request.POST["phonenumber"]
            form.save()
            return redirect("/")
    # method == 'GET' 일 때
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {"form": form}
    # 관련 템플릿에 기존 정보를 넘겨 준다
    return render(request, "tweet/edit.html", context)


# user profile update 페이지 /password_reset/ url 연결
def password(request):
    return redirect("/password_reset/")
