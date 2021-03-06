import random

from allauth.account.signals import user_signed_up  # type: ignore
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from cart.forms import AddProductForm
from plant.models import Plant
from product.models import Category, Product
from user.models import UsersFav


# request는 장고 뷰가 던져질때 자연스럽게 들어오는 request 객체를 이용
def product_in_category(request: HttpRequest, category_slug=None) -> HttpResponse:
    # 제품을 보여줄 수 있는 것만 불러오기
    products = Product.objects.filter(available_display=True)

    page = int(request.GET.get("page", 1) or 1)

    limit = 15
    offset = limit * (page - 1)

    product_category = []
    if category_slug:

        current_category = get_object_or_404(Category, slug=category_slug)

        for product in products:

            if current_category == product.category:
                product_category.append(product)

            else:
                pass
        products = product_category

    else:
        # 카테고리가 있을수도 없을수도있으니 None으로 설정
        current_category = None

    procuts_page = products
    # 피드 리스트 가져오기
    # products = Product.objects.filter(available_display=True)[offset:offset + limit]
    products = products[offset : offset + limit]

    # page_all_product = Product.objects.all()
    paginator = Paginator(procuts_page, "15")
    page_obj = paginator.get_page(page)

    # print(f"product_page_obj:{page_obj}")

    # Category 전체를 불러올것
    categories = Category.objects.all()

    # ###################################################################
    # 추천 식물 상품
    if not request.user.is_authenticated:
        sug_product = None
    else:
        user = request.user
        # 사용자 설문 조사 내용 가져오기
        userfav = UsersFav.objects.filter(user_id=user)
        plant_result = userfav[0].result1
        level_result = userfav[0].result2
        size_result = userfav[0].result3
        if plant_result == "식물":
            # 조건에 맞는 식물 쿼리셋 가져오기
            sug_plant = Plant.objects.exclude(type__contains="꽃").filter(grow_level=level_result, size=size_result)
        elif plant_result == "꽃":
            sug_plant = Plant.objects.filter(type__contains=plant_result, grow_level=level_result, size=size_result)
        # 예외처리
        else:
            sug_plant = []

        # 식물 정보를 가져왔으니 식물 정보랑 매핑되는 상품 정보 가져오자
        sug_product = []
        for plant in sug_plant:
            # 플랜트 모델과 포린키로 연결된 프로덕트를 가져오고
            product_list = Product.objects.filter(plant_id=plant)
            # 정보가 없다면 pass
            if len(product_list) == 0:
                pass
            # 정보가 있다면 해당 쿼리셋에서 상품을 뽑아서 sug_product에 넣어주자
            else:
                for product in product_list:
                    sug_product.append(product)

        # sug_product 갯수가 4개 미만이면 default 정보로 전환
        if len(sug_product) < 3:
            id_list = [307, 587, 75, 584, 467, 357, 583, 186, 234, 440]
            default_product_list = []
            for id in id_list:
                default_product = Product.objects.get(id=id)
                default_product_list.append(default_product)

            sug_product = default_product_list
        # sug_product 셔플
        random.shuffle(sug_product)
        # 셔플된 sug_product 에서 앞 4개만 변수에 저장
        # 사용자가 없는 경우 none 값을 넣기에 따로 변수에 담아서 클라이언트에 전달
        sug_product = sug_product[:3]
        # print(sug_product)
    # 추천 식물 상품 끝
    #####################################################################

    # get object or 는 말그대로 오브젝트를 가져오려고 시도해보고 없으면 404 에러를 나타내어 준다.
    # 밑의 내용은 category_slug를 Category 테이블의 slug에서 찾아보고 없다면 404가 뜨게된다

    ######################################################################################
    # templates의 구조에 따라서 다르게 쓸 수 있으나 앱기반으로 하여 이렇게 되어있다. 수정이 필요한 부분
    ######################################################################################

    total_len = len(procuts_page)
    pages = request.GET.get("page", 1)
    paginator = Paginator(procuts_page, 15)
    try:
        lines = paginator.page(pages)
    except PageNotAnInteger:
        lines = paginator.page(1)
    except EmptyPage:
        lines = paginator.page(paginator.num_pages)
    index = lines.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0
    if index < 2:
        end_index = 5 - start_index
    else:
        end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range[start_index:end_index])

    return render(
        request,
        "product/list.html",
        {
            "current_category": current_category,
            "categories": categories,
            "products": products,
            "sug_product": sug_product,
            "page_obj": page_obj,
            "result_list": lines,
            "page_range": page_range,
            "total_len": total_len,
            "max_index": max_index - 2,
        },
    )


def product_detail(request: HttpRequest, id, product_slug=None) -> HttpResponse:
    product = get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductForm(initial={"quantity": 1})

    return render(request, "product/detail.html", {"product": product, "add_to_cart": add_to_cart})
