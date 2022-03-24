from django.db import models

from config.models import BaseModel
from plant.models import Plant


class ProductCategory(BaseModel):
    category = models.CharField(max_length=45)


class Product(BaseModel):
    # on_delete의 설정이 foreign key가 지워졌을때 제품도 지워지면 안되므로 .SET_NULL이 맞다고 생각합니다.
    # product_category_id = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, related_name='products')
    product_category_id = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_name="product", db_column="product_category_id"
    )
    plant_id = models.ForeignKey(
        Plant, on_delete=models.CASCADE, related_name="product", db_column="plant_id", null=True
    )
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    size = models.IntegerField(null=True, blank=True)
    info = models.CharField(max_length=500, null=True, blank=True)
    qty = models.IntegerField(default=0)
    image = models.CharField(max_length=256)
    image_tag = models.TextField(null=True, blank=True)


# from django.db import models
# from django.urls import reverse
#
#
# class Category(models.Model):
#     name = models.CharField(max_length=200, db_index=True)
#     meta_description = models.TextField(blank=True)
#
#     slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
#
#     class Meata:
#         ordering = ['name']
#         verbose_name = 'category'
#         verbose_name_plural = 'categories'
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse('shop:product_in_category', args=[self.slug])
#
#
# class Product(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
#     name = models.CharField(max_length=200, db_index=True)
#     slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
#
#     image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
#     description = models.TextField(blank=True)
#     meta_description = models.TextField(blank=True)
#
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock = models.PositiveIntegerField()
#
#     available_display = models.BooleanField('Display', default=True)
#     available_order = models.BooleanField('Order', default=True)
#
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#
#     class Meata:
#         ordering = ['-created']
#         index_together = [['id','slug']]
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse('shop:product_detail', args=[self.id, self.slug])
