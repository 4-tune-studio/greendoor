# pdf를 위한 임포트
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.generic.base import View

from cart.cart import Cart

from .forms import *
from .models import *

# import weasyprint


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        print("1번구역")
        if form.is_valid():
            order = form.save(commit=False)
            # if cart.coupon:
            #     order.coupon = cart.coupon
            #     order.discount = cart.coupon.amount
            print("2번구역")
            order.save()
            for item in cart:
                print("3번구역")
                OrderItem.objects.create(
                    order=order, product=item["product"], price=item["price"], quantity=item["quantity"]
                )
            cart.clear()
            return render(request, "order/create.html", {"order": order})
    else:
        print("4번구역")
        form = OrderCreateForm()
    return render(request, "order/create.html", {"cart": cart, "form": form})


def order_complete(request):
    order_id = request.GET.get("order_id")
    order = Order.objects.get(id=order_id)
    return render(request, "order/complete.html", {"order": order})


class OrderCreateAjaxView(View):
    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            print("권한이 없을때")
            return JsonResponse({"authenticated": False}, status=403)

        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        print(f"form: {form}")

        if form.is_valid():
            print("5번 구역")
            order = form.save(commit=False)
            # if cart.coupon:
            #     order.coupon = cart.coupon
            #     order.discount = cart.coupon.amount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order, product=item["product"], price=item["price"], quantity=item["quantity"]
                )
            cart.clear()
            data = {"order_id": order.id}
            return JsonResponse(data)
        else:
            print("6번 구역")
            return JsonResponse({}, status=401)


class OrderCheckoutAjaxView(View):
    def post(self, request, *args, **kwargs):
        print("11번 구역")
        if not request.user.is_authenticated:
            print("12번 구역")
            return JsonResponse({"authenticated": False}, status=403)

        order_id = request.POST.get("order_id")
        # print(f"order_id :{order_id}")

        # print(f"==================================")
        order = Order.objects.get(id=order_id)
        print(f"order:{order}")
        # print(f"order :{order}")
        amount = request.POST.get("amount")
        print(f"amount:{amount}")
        try:
            print("13번 구역")
            merchant_order_id = OrderTransaction.objects.create_new(order=order, amount=amount)
            print(merchant_order_id)
        except:
            print("14번 구역")
            merchant_order_id = None

        if merchant_order_id is not None:
            data = {"works": True, "merchant_id": merchant_order_id}
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)


class OrderImpAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated": False}, status=403)

        order_id = request.POST.get("order_id")
        order = Order.objects.get(id=order_id)
        merchant_id = request.POST.get("merchant_id")
        imp_id = request.POST.get("imp_id")
        amount = request.POST.get("amount")

        try:
            trans = OrderTransaction.objects.get(order=order, merchant_order_id=merchant_id, amount=amount)
        except:
            trans = None

        if trans is not None:
            trans.transaction_id = imp_id
            trans.success = True
            trans.save()
            order.paid = True
            order.save()

            data = {"works": True}

            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "admin/detail.html", {"order": order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string("admin/pdf.html", {"order": order})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "filename=order_{}.pdf".format(order.id)
    # weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATICFILES_DIRS[0]+'/css/pdf.css')])
    return response
