from django.http import HttpRequest, HttpResponse, JsonResponse

from .cart import Cart


def cart(request: HttpRequest) :
    cart = Cart(request)
    return {"cart": cart}
