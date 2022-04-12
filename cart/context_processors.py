from django.http import HttpRequest

from .cart import Cart


def cart(request: HttpRequest):
    cart = Cart(request)
    return {"cart": cart}
