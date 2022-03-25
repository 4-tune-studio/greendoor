from allauth.account.signals import user_signed_up  # type: ignore
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, render

from cart.forms import AddProductForm

from .models import *


# request는 장고 뷰가 던져질때 자연스럽게 들어오는 request 객체를 이용
def product_in_category(request, category_slug=None):
    # 카테고리가 있을수도 없을수도있으니 None으로 설정
    current_category = None
    # Category 전체를 불러올것
    categories = Category.objects.all()
    # 제품을 보여줄 수 있는 것만 불러오기
    products = Product.objects.filter(available_display=True)

    # get object or 는 말그대로 오브젝트를 가져오려고 시도해보고 없으면 404 에러를 나타내어 준다.
    # 밑의 내용은 category_slug를 Category 테이블의 slug에서 찾아보고 없다면 404가 뜨게된다
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    ######################################################################################
    # templates의 구조에 따라서 다르게 쓸 수 있으나 앱기반으로 하여 이렇게 되어있다. 수정이 필요한 부분
    ######################################################################################
    return render(
        request,
        "shop/list.html",
        {
            "current_category": current_category,
            "categories": categories,
            "products": products,
        },
    )


def product_detail(request, id, product_slug=None):
    product = get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductForm(initial={"quantity": 1})
    return render(request, "shop/detail.html", {"product": product, "add_to_cart": add_to_cart})


@receiver(user_signed_up)
def user_signed_up_(**kwargs):
    user = kwargs["user"]
    extra_data = user.socialaccount_set.filter(provider="naver")[0].extra_data
    user.last_name = extra_data["name"][0:4]
    user.first_name = extra_data["name"][4:]
    user.save()
