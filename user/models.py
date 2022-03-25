from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models

# Create your models here.
from config.models import BaseModel


class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30)
    image = models.CharField(max_length=256)
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

    pass


class UserImg(BaseModel):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="user/%Y%m%d", max_length=255)
