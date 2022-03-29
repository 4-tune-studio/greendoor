from django.contrib import admin

from .models import *


class CategoryAdmin(admin.ModelAdmin[Category]):
    # 보여줄것 목록
    list_display = ["id", "name", "slug"]
    # 제품을 등록할때 자동으로 만들어서 등록할 값 밑에 내용으로는 name을 만들면 slug도 만들어줌
    # ('name',) 값의 형태로 되어있지만 ['name']으로도 변경 가능
    prepopulated_fields = {"slug": ["name"]}


# 첫번째 인수가 등록할 클래스 두번째 인자는 해당 내용을 어떻게 보여줄 것인가를 만들어서 등록
# admin.site.register()
admin.site.register(Category, CategoryAdmin)


# annotation 기법, 데코레이터라고 부르기도 함


class ProductAdmin(admin.ModelAdmin[Product]):
    list_display = [
        "name",
        "slug",
        "category",
        "price",
        "stock",
        "available_display",
        "available_order",
        "created_at",
        "updated_at",
    ]
    # 필터가 걸리는 영역
    list_filter = ["available_display", "created_at", "updated_at", "category"]
    # 제품을 등록할때 자동으로 만들어서 등록할 값 밑에 내용으로는 name을 만들면 slug도 만들어줌
    # ('name',) 값의 형태로 되어있지만 ['name']으로도 변경 가능
    prepopulated_fields = {"slug": ["name"]}
    # 목록에서 자주 바꾸는 것은 이곳을 통하여 변환
    list_editable = ["price", "stock", "available_display", "available_order"]


admin.site.register(Product, ProductAdmin)
