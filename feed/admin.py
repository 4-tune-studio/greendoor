from django.contrib import admin

from feed.models import Feed, FeedBookmark, FeedComment, FeedLike, Img

# Register your models here.

admin.site.register(Feed)
admin.site.register(FeedBookmark)
admin.site.register(FeedLike)
admin.site.register(FeedComment)
admin.site.register(Img)
