from feed.models import Feed
from django.db.models import Q

from feed.services.feed_service import (
    get_feed_list,
    get_popular_feed_list,
)
from allauth.account.signals import user_signed_up  # type: ignore
from django.shortcuts import get_object_or_404, render, redirect

from product.models import Category, Product

URL_COMMUNITY = "feed:community"


# filter 함수의 Q함수: OR조건으로 데이터를 조회하기 위해 사용하는 함수
# objects.filter() 는 특정 조건에 해당하면 객체 출력 .get('kw') 은 kw만 반환
# __icontains 연산자 : 대소문자를 구분하지 않고 단어가 포함되어 있는지 검사. 사용법 "필드명"__icontains = 조건값

def feed_searchResult(request):
    if 'kw' in request.GET:
        query = request.GET.get('kw')
        search_feeds = Feed.objects.all().filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

        if request.user.is_authenticated:
            user_id = request.user.id
        # 로그인이 되어있지 않다면
        else:
            # 없는 사용자 id
            user_id = 0

        # 클라이언트에서 전해준 page 값을 저장 (default : none -> 1, "" -> 1)
        page = int(request.GET.get("page", 1) or 1)
        limit = 40
        offset = limit * (page - 1)

        # 피드 리스트 가져오기
        all_feed = get_feed_list(user_id, offset, limit)

        # 첫 페이지라면
        if offset == 0:
            popular_feeds = get_popular_feed_list(user_id, offset, 20)
            return render(request, "index.html", {"all_feed": all_feed, "popular_feeds": popular_feeds, 'query': query,
                                                  'search_feeds': search_feeds})

        return render(request, "index.html", {"all_feed": all_feed, 'query': query, 'search_feeds': search_feeds})

        # 다른 방식으로 요청이 오면 index 페이지로 리다이렉트
    else:
        return redirect(URL_COMMUNITY)


def product_searchResult(request, category_slug=None):
    if 'kw' in request.GET:
        query = request.GET.get('kw')
        search_products = Product.objects.all().filter(
            Q(name__icontains=query) |
            Q(slug__icontains=query)
        )
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
    return render(
        request,
        "product/list.html",
        {
            "current_category": current_category,
            "categories": categories,
            "products": products,
            'query': query,
            'search_products': search_products,
        },
    )
