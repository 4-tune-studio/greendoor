from django.contrib import admin
from info.models import Info
from embed_video.admin import AdminVideoMixin


# Register your models here.
class InfoAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ("title", "video")


admin.site.register(Info, InfoAdmin)