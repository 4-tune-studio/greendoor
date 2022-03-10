from django.db import models

from greendoor.models import BaseModel


# === plant 앱에 포함 ===
class PlantCategory(BaseModel):
    category = models.CharField(max_length=45)


class Plant(BaseModel):
    plant_category_id = models.ForeignKey(PlantCategory, on_delete=models.CASCADE, related_name="plant",
                                          db_column="plant_category_id")
