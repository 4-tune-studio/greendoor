import json
import random

from allauth.account.signals import user_signed_up  # type: ignore
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from feed.models import Feed
from feed.services.feed_service import get_feed_list, get_popular_feed_list
from plant.models import Plant
from product.models import Category, Product
from user.models import UsersFav

URL_COMMUNITY = "feed:community"


# filter 함수의 Q함수: OR조건으로 데이터를 조회하기 위해 사용하는 함수
# objects.filter() 는 특정 조건에 해당하면 객체 출력 .get('kw') 은 kw만 반환
# __icontains 연산자 : 대소문자를 구분하지 않고 단어가 포함되어 있는지 검사. 사용법 "필드명"__icontains = 조건값


def feed_searchResult(request):
    if "kw" in request.GET:
        query = request.GET.get("kw")
        search_feeds = Feed.objects.all().filter(Q(title__icontains=query) | Q(content__icontains=query))

        if request.user.is_authenticated:
            user_id = request.user.id
        # 로그인이 되어있지 않다면
        else:
            # 없는 사용자 id
            user_id = 0

        # 클라이언트에서 전해준 page 값을 저장 (default : none -> 1, "" -> 1)
        page = int(request.GET.get("page", 1) or 1)
        limit = 18
        offset = limit * (page - 1)

        # 피드 리스트 가져오기
        all_feed = get_feed_list(user_id, offset, limit)

        # 첫 페이지라면
        if offset == 0:
            popular_feeds = get_popular_feed_list(user_id, offset, 6)
            return render(
                request,
                "index.html",
                {"all_feed": all_feed, "popular_feeds": popular_feeds, "query": query, "search_feeds": search_feeds},
            )

        # 비동기식
        # offset이 0이 아닐경우 // ajax로 2가 넘어오면 1
        data = serializers.serialize("json", list(all_feed))
        context = {"all_feed": all_feed}
        return HttpResponse(json.dumps(data), content_type="application/json")

        # 다른 방식으로 요청이 오면 index 페이지로 리다이렉트
    else:
        return redirect(URL_COMMUNITY)


def product_searchResult(request, category_slug=None):
    if "kw" in request.GET:
        query = request.GET.get("kw")
        search_products = Product.objects.all().filter(Q(name__icontains=query) | Q(slug__icontains=query))
    # 제품을 보여줄 수 있는 것만 불러오기
    products = Product.objects.filter(available_display=True)
    # Category 전체를 불러올것
    categories = Category.objects.all()

    # get object or 는 말그대로 오브젝트를 가져오려고 시도해보고 없으면 404 에러를 나타내어 준다.
    # 밑의 내용은 category_slug를 Category 테이블의 slug에서 찾아보고 없다면 404가 뜨게된다
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)
    else:
        # 카테고리가 있을수도 없을수도있으니 None으로 설정
        current_category = None

    ######################################################################################
    # templates의 구조에 따라서 다르게 쓸 수 있으나 앱기반으로 하여 이렇게 되어있다. 수정이 필요한 부분
    ######################################################################################
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

    return render(
        request,
        "product/list.html",
        {
            "current_category": current_category,
            "categories": categories,
            "products": products,
            "query": query,
            "search_products": search_products,
            "sug_product": sug_product,
        },
    )
