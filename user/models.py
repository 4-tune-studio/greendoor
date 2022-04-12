from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models

from config.models import BaseModel

# Create your models here.


class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    nickname = models.CharField(max_length=30)
    image = models.CharField(max_length=256, default="https://greendoorhope.s3.amazonaws.com/img/profile.jpg")
    zipcode = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    phonenumber = models.CharField(max_length=11, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"  # email을 사용자의 식별자로 설정
    REQUIRED_FIELDS = ["username"]  # 필수입력값


class UsersFav(BaseModel):
    user_id = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="fav", db_column="user_id")
    result1 = models.CharField(max_length=100)
    result2 = models.CharField(max_length=100)
    result3 = models.CharField(max_length=100)


class UserImg(BaseModel):
    img = models.ImageField(upload_to="user/%Y%m%d", max_length=255)
