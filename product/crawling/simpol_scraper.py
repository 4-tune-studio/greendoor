# ####################################
# simpol 사이트 식물 상품 스크래핑
# ####################################
# 카테고리 code
#
# 다육식물/선인장 : code=004
# 관엽식물/공기정화식물 : code=003
# 야생화/허브/수생식물/채소/동백 : code=005
# 분재/분경/수석 : code=006
# 동서양란 : code=007
# 묘목/조경/인테리어 : code=008
# 꽃배달/생화/드라이플라워/비누꽃 : code=002
# 화분자재류 : code=009
# 원예자재류 : code=022
# ####################################
# 스크래핑 해야 할 product 정보
# name/slug/image/price/ (info)
# ####################################

# 장고 프로젝트에서 일반 python 파일을 사용할 수 있게 설정
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

import requests
from bs4 import BeautifulSoup

from plant.models import Plant
from product.models import Product

# 헤더 지정
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}

'''
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                   카테고리에서 상품 추출
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# -------------- 카테고리 추출 설정 (시작)-------------- #

# 카테고리 코드 // for문에 넣어서 카테고리 전부 스크래핑
CODE_LIST = ["004", "003", "005", "006", "007"]
CODE = "004"

# 기본 url
URL = f"https://www.simpol.co.kr/front/productlist.php?code={CODE}"

# -------------- 카테고리 추출 설정 (끝)-------------- #


# -------------- 카테고리의 마지막 페이지 추출 (시작)-------------- #

# url로 requests 요청
result = requests.get(f"{URL}", headers=HEADERS)
# request status code 출력
print(f"status code: {result.status_code}")

# bs4 패키지를 이용해서 requests한 내용 파싱
soup = BeautifulSoup(result.text, "html.parser")

# 페이지 정보를 가지고 있는 태그 추출
paginate = soup.find("div", {"class": "paginate"})
print(paginate)

# 마지막 페이지
last_page = int(paginate.find("a", {"class": "next_end"})["href"].split("(")[1].split(")")[0])
print(last_page)
print(type(last_page))

# -------------- 카테고리의 마지막 페이지 추출 (끝)-------------- #

# -------------- 페이지 스크래핑 (시작)-------------- #

# for page in range(1, last_page + 1):
page_result = requests.get(f"{URL}&page=1", headers=HEADERS)
# 인코딩 추측을 하지 않도록 None 지정 (UTF-8, EUC-KR 로 지정해도 된다)
page_result.encoding = None
# 작업 페이지 및 status 확인
print(f"-------- 1page 추출 중 -------- status: {page_result.status_code}")
soup = BeautifulSoup(page_result.text, "html.parser")
# 상품 url을 담고 있는 div list
products = soup.find_all("div", {"class": "goods_name txt_limit"})

# 상품 페이지 기본 url
PRODUCT_URL = "https://www.simpol.co.kr/front/"
IMAGE_URL = "https://www.simpol.co.kr/"
# list에서 a 태그의 href를 추출
for p in products:
    product = p.find("a")["href"]
    # title 정보 변수 저장
    title = p.find("a").text.strip().replace("/", ",")
    # 상품 url로 requests
    product_result = requests.get(f"{PRODUCT_URL}{product}", headers=HEADERS)
    product_result.encoding = None
    # requests status 확인
    # print(f"status code: {product_result.status_code}")
    soup = BeautifulSoup(product_result.text, "html.parser")
    # price 정보 변수에 저장
    price = int(soup.find("span", {"id": "idx_price"}).text.rstrip("원").replace(",", ""))
    # image 정보 병수에 저장
    image = soup.find("img", {"class": "txc-image"})["src"].split("?")[0]

    # info의 경우 줄바꿈, 공백 문제를 해결해야 함
    # info = soup.find("div", {"class": "insert_content"}).getText
    print(title)
    print(price)
    print(IMAGE_URL + image)
    # print(info)

    # DB Product 테이블에 정보 저장
    Product.objects.create(category_id=1, name=title, slug=title, image=IMAGE_URL + image, price=price)

# -------------- 페이지 스크래핑 (끝)-------------- # 
'''

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                   WORD로 검색해서 추출
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# -------------- 단어 검색 추출 설정 (시작)-------------- #

# 검색 키워드 가져오기
WORDS = Plant.objects.all()

# 단어로 검색 url
WORD = "이상한거"
URL = f"https://www.simpol.co.kr/front/productsearch.php?&search={WORD}"

# -------------- 단어 검색 추출 설정 (끝)-------------- #

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WORD로 스크래핑 할 경우 word당 1~3건 정도의 데이터만 필요하기에 last 페이지 추출할 필요는 없음
# 대신 word로 검색 시 자료가 없는 경우 예외처리를 해줘야함
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# -------------- 페이지 스크래핑 (시작)-------------- #

page_result = requests.get(f"{URL}", headers=HEADERS)
# 인코딩 추측을 하지 않도록 None 지정 (UTF-8, EUC-KR 로 지정해도 된다)
page_result.encoding = None
# 작업 페이지 및 status 확인
print(f"-------- {WORD} 추출 중 -------- status: {page_result.status_code}")
soup = BeautifulSoup(page_result.text, "html.parser")

# 상품 url을 담고 있는 div list // 해당 class의 div가 없는 경우 pass (따로 예외처리를 안해도 된다???)
products = soup.find_all("div", {"class": "goods_name txt_limit"})

# 상품 정보 리스트가 비어있으면 pass
if len(products) == 0:
    # TODO 위에 단어 고르는 for문 넣으면 break로 바꾸기
    pass
# 정보가 있을때만 스크래핑 시작
else:
    # 상품 페이지 기본 url
    PRODUCT_URL = "https://www.simpol.co.kr/front/"
    # 이미지 기본 url
    IMAGE_URL = "https://www.simpol.co.kr/"

    # list에서 a 태그의 href를 추출
    for p in products:
        product = p.find("a")["href"]
        # title 정보 변수 저장
        title = p.find("a").text.strip().replace("/", ",")
        # 상품 url로 requests
        product_result = requests.get(f"{PRODUCT_URL}{product}", headers=HEADERS)
        product_result.encoding = None
        # requests status 확인
        # print(f"status code: {product_result.status_code}")
        soup = BeautifulSoup(product_result.text, "html.parser")
        # price 정보 변수에 저장
        price = int(soup.find("span", {"id": "idx_price"}).text.rstrip("원").replace(",", ""))
        # image 정보 병수에 저장
        image = soup.find("img", {"class": "txc-image"})["src"].split("?")[0]

        # info의 경우 줄바꿈, 공백 문제를 해결해야 함
        # info = soup.find("div", {"class": "insert_content"}).getText
        print(title)
        print(price)
        print(IMAGE_URL + image)
        # print(info)
        # DB Product 테이블에 정보 저장
        # Product.objects.create(category_id=1, name=title, slug=title, image=IMAGE_URL + image, price=price)

# -------------- 페이지 스크래핑 (끝)-------------- #