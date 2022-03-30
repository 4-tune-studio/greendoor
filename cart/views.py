from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from product.models import Product

from .cart import Cart
from .forms import AddProductForm


# 데코레이터 의미 POST method만으로 접속이 가능하다
@require_POST

def add(request: HttpRequest, product_id: int) -> HttpResponse:
    print(type(product_id))

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    # 클라이언트 -> 서버로 데이터를 전달
    # 유효성 검사, injection 전처리
    form = AddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd["quantity"], is_update=cd["is_update"])
    # if문 밖으로 return을 하는 것은 장바구니에 물품이 있는지와 상관없이 내용을 확인 할 수 있게 하기 위해
    return redirect("cart:detail")



def remove(request: HttpRequest, product_id: str) -> HttpResponse:
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:detail")


def detail(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    for product in cart:
        product["quantity_form"] = AddProductForm(initial={"quantity": product["quantity"], "is_update": True})

    return render(request, "cart/detail.html", {"cart": cart})

