
# ####################################
# simpol 사이트 식물 상품 스크래핑
#
#
#
# ####################################


import django
import os
import requests

from time import sleep

from bs4 import BeautifulSoup

from product.models import Category, Product

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}

WORD = "플랜테리어"
URL = f"https://www.ssg.com/search.ssg?target=all&query={WORD}&count=100&display=img&page="
last_pages = 2

product_url_head = "https://www.ssg.com"