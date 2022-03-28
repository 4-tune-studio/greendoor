from django.db import models
from django.urls import reverse

from config.models import BaseModel
from plant.models import Plant

# class ProductCategory(BaseModel):
#     category = models.CharField(max_length=45)

# 밑에 새로 생성
# class Product(BaseModel):
#     # on_delete의 설정이 foreign key가 지워졌을때 제품도 지워지면 안되므로 .SET_NULL이 맞다고 생각합니다.
#     # product_category_id = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, related_name='products')
#
#     name = models.CharField(max_length=100)
#     price = models.IntegerField()
#     size = models.IntegerField(null=True, blank=True)
#     info = models.CharField(max_length=500, null=True, blank=True)
#     qty = models.IntegerField(default=0)
#     image = models.CharField(max_length=256)
#     image_tag = models.TextField(null=True, blank=True)


class Category(models.Model):
    # db_index 검색이 가능하게 설정
    name = models.CharField(max_length=200, db_index=True)
    # SEO 검색엔진에 제출될 정보, 내용이 blank 없어도 됨
    meta_description = models.TextField(blank=True)
    # 글번호, 제품 번호등 PK로 접근하는 것이 아닌 카테고리 이름등을 통해 접근하기 위한 값
    # db_index PK로 사용할 수 있기 때문에 allow_unicode 한글로 사용할 수 있게 하기 위해
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    class Meta:
        # 이름순으로 정렬 없으면 id 값으로 정렬해야함
        ordering = ["name"]
        # admin이나 이렇게 노출될때 단수형 이름
        verbose_name = "category"
        # admin이나 이렇게 노출될때 복수형 이름
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        # 카테고리를 출력하게 되면 나타낼 값을 그 카테고리의 이름으로 설정
        return self.name

    # 상세 페이지등을 결정해주는 것
    def get_absolute_url(self) -> str:
        # 보통은 해당 인스턴스의 디테일 페이지를 가르키는 형태로 작성함 reverse import해와서 사용
        # product:product_in_category , product이라는 네임스페이스 안에서 product_in_category 불러옴
        # self.slug 이용하여 불러옴
        return reverse("product:product_in_category", args=[self.slug])


class Product(BaseModel):
    # on_delete 셋 널로 해서 카테고리가 지워져도 지워지지 않게 설정
    # 옵션 일부 수정함 db_column 삭제 가능 여부 확인 필요
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    # db_column 이 없으면 앞에 적힌 필드 값에 _id로 만들어주는것을 내가 알아서 설정하기 위함

    # 이 내용은 삭제 예정 3/26
    # plant_id = models.ForeignKey(
    #     Plant, on_delete=models.SET_NULL, related_name="products", db_column="plant_id", null=True
    # )

    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True, default="")

    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    description = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)

    # DecimalField는 사용안하고 IntegerField로 해도 상관 없다.
    # decimal_places 소수점
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # 남은 숫자 확인을 위한 stock 설정
    stock = models.PositiveIntegerField(default=0)

    available_display = models.BooleanField("Display", default=True)
    available_order = models.BooleanField("Order", default=True)

    # BASE model 상속 받는 것으로 대체함
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

    # 추가된 필드 내용
    size = models.IntegerField(null=True, blank=True)
    info = models.CharField(max_length=500, null=True, blank=True)

    # 삭제예정 Stock으로 대체 3/26
    # qty = models.IntegerField(default=0)
    image_tag = models.TextField(null=True, blank=True)

<<<<<<< HEAD

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
=======
    # class Meta 잠시 설명 nastied class라고 하여 다양한 정보를 품고 있다 이런 뜻으로 검색 옵션 디스플레이되는 이름등의 정보를 담고 있음
    class Meta:
        ordering = ["-created_at"]
        # 두개를 병합해서 inex 기준을 정해주는 부분
        index_together = [["id", "slug"]]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("product:product_detail", args=[self.id, self.slug])
>>>>>>> 813c772df3dcf24466e3f1fe2187bbed5e7bb616
