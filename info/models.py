from django.db import models
from embed_video.fields import EmbedVideoField

from config.models import BaseModel


class Info(BaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    video = EmbedVideoField()
