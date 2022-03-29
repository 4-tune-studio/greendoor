from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

app_name = "user"

urlpatterns = [
    # =============== 장고 인증 URL + 템플릿 연결 ================ #
    # 장고 URL -> 로그인 템플릿 연결 버튼
    path("accounts/login/", views.accounts_login, name="accounts-login"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="password/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(template_name="password/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(template_name="password/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path("sign-up/", views.sign_up_view, name="sign-up"),
    path("sign-in/", views.sign_in_view, name="sign-in"),
    path("logout/", views.logout, name="logout"),
    path("google/", include("allauth.urls")),
    # =============== user profile update ================ #
    path("user/profile_edit/<int:pk>", views.profile_edit, name="profile_edit"),
    path("password/", views.password, name="password"),
    path("user/api_update_user_image", views.api_update_user_image, name="api_update_user_image"),
    path("user/my_page/<int:pk>", views.user_my_page, name="user_my_page"),
]
