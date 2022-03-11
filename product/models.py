from django.db import models

from greendoor.models import BaseModel
from plant.models import Plant


class ProductCategory(BaseModel):
    category = models.CharField(max_length=45)


class Product(BaseModel):
    product_category_id = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_name="product", db_column="product_category_id"
    )
    plant_id = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="product", db_column="plant_id",
                                 null=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    size = models.IntegerField()
    info = models.CharField(max_length=500)
    qty = models.IntegerField(default=0)
    image = models.CharField(max_length=256)
    image_tag = models.TextField(null=True, blank=True)
