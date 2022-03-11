from time import sleep

import requests
from bs4 import BeautifulSoup

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greendoor.settings")

import django
django.setup()

from product.models import Product, ProductCategory


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}

WORD = "플랜테리어"
URL = f"https://www.ssg.com/search.ssg?target=all&query={WORD}&count=100&display=img&page="
last_pages = 2

product_url_head = "https://www.ssg.com"

# 찾아야 되는거 : 상품 주소 / 상품 주소 내 제목, 가격, 상세페이지 html태그


# 모든 페이지 실행
# 0~last p -1 까지
infos = []
for page in range(last_pages):
    print(f"SGG 추출중 ... {page + 1}p")
    result = requests.get(f"{URL}{page + 1}", headers=headers)
    print(f"status code: {result.status_code}")
    soup = BeautifulSoup(result.text, "html.parser")

    div_box = soup.find_all("div", {"class": "thmb"})

    product_link_list = []
    for thmb in div_box:
        link = thmb.find("a")["href"]
        product_link_list.append(link)

    i = 0
    for product_link in product_link_list:
        product = product_url_head + product_link
        product_result = requests.get(f"{product}", headers=headers)
        product_soup = BeautifulSoup(product_result.text, "html.parser")

        title = product_soup.find("h2", {"class": "cdtl_info_tit"}).text  # text or string ?
        # print(title)
        price = product_soup.find("em", {"class": "ssg_price"}).text
        price = int(price.replace(",", ""))
        # print(price)
        main_image = product_soup.find("img", {"id": "mainImg"})["src"]
        # print(main_image)
        try:
            detail = product_soup.find("div", {"class": "cdtl_sec cdtl_seller_html"}).find("iframe")["src"]
            # print(detail)
            detail_result = requests.get(f"{detail}", headers=headers)
            detail_soup = BeautifulSoup(detail_result.text, "html.parser")
            img_tag = detail_soup.find_all("img")
        except AttributeError:
            img_tag = None
        # print(img_list)

        img_tag = str(img_tag).strip("[]")
        img_tag = img_tag.replace(',', '')
        # print(img_tag)
        # print(str(img_tag).strip('[]'))

        main_image = f"https:{main_image}"


        product_category_id = ProductCategory.objects.get(id=1)

        Product.objects.create(
            product_category_id=product_category_id,
            name=title,
            price=price,
            image=main_image,
            image_tag=img_tag
        )

        info = {"title": title, "price": price, "main_image": main_image, "img_tag": img_tag}
        infos.append(info)
        i += 1
        print(f"{i} clear")
        sleep(3)

print(infos)
