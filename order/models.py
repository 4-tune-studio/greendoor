from django.db import models

from greendoor.models import BaseModel
from product.models import Product
from user.models import Users


class OrderBasket(BaseModel):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="order_basket", db_column="user_id")
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_basket", db_column="product_id"
    )
    qty = models.IntegerField()


class Order(BaseModel):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="order", db_column="user_id")
    status = models.IntegerField(default=2)  # 처리중-2, 완료-1, 실패-0


class OderProduct(BaseModel):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_product", db_column="order_id")
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_product", db_column="product_id"
    )
    qty = models.IntegerField()
