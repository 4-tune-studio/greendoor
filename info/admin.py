from django.contrib import admin
from embed_video.admin import AdminVideoMixin

from info.models import Info


# Register your models here.
class InfoAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ("title", "video")


admin.site.register(Info, InfoAdmin)
