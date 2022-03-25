from django.contrib import admin

from user.models import UserImg, Users

# Register your models here.
admin.site.register(Users)
admin.site.register(UserImg)
