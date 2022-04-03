from django.contrib import admin

from .models import Choice, Level, Question

# Register your models here.

admin.site.register(Level)
admin.site.register(Question)
admin.site.register(Choice)
