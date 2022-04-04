from django.urls import path

from .views import *

# 네임 스페이스로 동일하게 사용가능
app_name = "product"
urlpatterns = [
    path("", product_in_category, name="product_all"),
    # category_slug는 views에 있는 변수명을 그대로 가져와서 사용
    # < 형식: 파라미터 > 형태로 사용 형식부분은 빠져도 가능 10,11번째줄을 비교하면 알 수 있음
    path("<slug:category_slug>/", product_in_category, name="product_in_category"),
    path("<int:id>/<product_slug>/", product_detail, name="product_detail"),
]
