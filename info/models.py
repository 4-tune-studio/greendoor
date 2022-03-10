from django.db import models

from greendoor.models import BaseModel


class Info(BaseModel):
    url = models.CharField(max_length=256)
