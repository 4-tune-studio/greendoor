# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# import urllib.request
import requests
from bs4 import BeautifulSoup

#####################################################################
# bs4 사용법 요약

# from bs4 import BeautifulSoup
# html = """<html><head></head><body>test data</body></html> """
# soup = BeautifulSoup(html, 'html.parser')
# print(soup.select_one('body').text)
#####################################################################


for i in range(1, 23):
    print(f"========================= {i}:page 시작 =========================")
    url = f"http://api.nongsaro.go.kr/sample/ajax/ajax_local_callback.jsp?garden/gardenList?apiKey=nongsaroSampleKey&htmlArea=nongsaroApiLoadingAreaResult&pageNo={i}&serviceType=ajaxType"

    html_txt = requests.get(url).text
    # print("page test")
    # print(json_txt)
    # print("=============================================== end page test")
    soup = BeautifulSoup(html_txt, "html.parser")
    # category_tr = soup.select('table.grid > tbody > tr > td')
    # print("category_tr test")
    # print(category_tr)
    # print("=============================================== end page test")
    for j in range(10):
        try:
            tr = soup.select("td > a")[j]["onclick"]
            tr = tr.lstrip("fncDtl(")
            tr = tr.strip().rstrip("eslaf nruter ;)")
            content_number = tr.replace("'", "")

            url = f"http://api.nongsaro.go.kr/sample/ajax/ajax_local_callback.jsp?garden/gardenDtl?apiKey=nongsaroSampleKey&htmlArea=nongsaroApiLoadingAreaResult&pageNo={i}&cntntsNo={content_number}&serviceType=ajaxType"
            content_html = requests.get(url).text

            content = BeautifulSoup(content_html, "html.parser")

            botanical_name = content.select("tr > td")[0].text
            english_name = content.select("tr > td")[1].text
            general_name = content.select("tr > td")[2].text
            type_name = content.select("tr > td")[3].text
            origin = content.select("tr > td")[4].text
            advise_info = content.select("tr > td")[5].text
            image_link = content.select("tr > td")[6].text
            heigt_info = content.select("tr > td")[7].text
            width_info = content.select("tr > td")[8].text
            leaftype_info = content.select("tr > td")[9].text

            smell_info = content.select("tr > td")[10].text
            toxic_info = content.select("tr > td")[11].text
            breeding_info = content.select("tr > td")[12].text
            extraperiod_info = content.select("tr > td")[13].text
            grow_level = content.select("tr > td")[14].text
            growth_speed = content.select("tr > td")[15].text
            growth_temp = content.select("tr > td")[16].text
            lowest_temp = content.select("tr > td")[17].text
            humidity = content.select("tr > td")[18].text
            fertilizer_info = content.select("tr > td")[19].text

            soil_info = content.select("tr > td")[20].text
            water_spring = content.select("tr > td")[21].text
            water_summer = content.select("tr > td")[22].text
            water_fall = content.select("tr > td")[23].text
            water_winter = content.select("tr > td")[24].text
            insect_info = content.select("tr > td")[25].text
            extragrow_info = content.select("tr > td")[26].text
            functional_info = content.select("tr > td")[27].text
            potsize_big = content.select("tr > td")[28].text
            potsize_mid = content.select("tr > td")[29].text

            potsize_small = content.select("tr > td")[30].text
            width_big = content.select("tr > td")[31].text
            width_mid = content.select("tr > td")[32].text
            width_small = content.select("tr > td")[33].text
            length_big = content.select("tr > td")[34].text
            length_mid = content.select("tr > td")[35].text
            length_small = content.select("tr > td")[36].text
            heigt_big = content.select("tr > td")[37].text
            heigt_mid = content.select("tr > td")[38].text
            heigt_small = content.select("tr > td")[39].text

            volume_big = content.select("tr > td")[40].text
            volume_mid = content.select("tr > td")[41].text
            volume_small = content.select("tr > td")[42].text
            price_big = content.select("tr > td")[43].text
            price_mid = content.select("tr > td")[44].text
            price_small = content.select("tr > td")[45].text
            care_need = content.select("tr > td")[46].text
            type = content.select("tr > td")[47].text
            growth_type = content.select("tr > td")[48].text
            indoor_garden = content.select("tr > td")[49].text

            ecology = content.select("tr > td")[50].text
            leaf_pattern = content.select("tr > td")[51].text
            leaf_color = content.select("tr > td")[52].text
            flower_season = content.select("tr > td")[53].text
            flower_color = content.select("tr > td")[54].text
            fluit_season = content.select("tr > td")[55].text
            fluit_color = content.select("tr > td")[56].text
            breeding_way = content.select("tr > td")[57].text
            lux = content.select("tr > td")[58].text
            location = content.select("tr > td")[59].text

            insect = content.select("tr > td")[60].text
            print(f"*********** {i} page {j+1} 번째 conetent ***********")
            print(botanical_name)
            print(english_name)
            print(general_name)
            print(type_name)
            print(origin)
            print(advise_info)
            print(image_link)
            print(heigt_info)
            print(width_info)
            print(leaftype_info)

            print(smell_info)
            print(toxic_info)
            print(breeding_info)
            print(extraperiod_info)
            print(grow_level)
            print(growth_speed)
            print(growth_temp)
            print(lowest_temp)
            print(humidity)
            print(fertilizer_info)

            print(soil_info)
            print(water_spring)
            print(water_summer)
            print(water_fall)
            print(water_winter)
            print(insect_info)
            print(extragrow_info)
            print(functional_info)
            print(potsize_big)
            print(potsize_mid)

            print(potsize_small)
            print(width_big)
            print(width_mid)
            print(width_small)
            print(length_big)
            print(length_mid)
            print(length_small)
            print(heigt_big)
            print(heigt_mid)
            print(heigt_small)

            print(volume_big)
            print(volume_mid)
            print(volume_small)
            print(price_big)
            print(price_mid)
            print(price_small)
            print(care_need)
            print(type)
            print(growth_type)
            print(indoor_garden)

            print(ecology)
            print(leaf_pattern)
            print(leaf_color)
            print(flower_season)
            print(flower_color)
            print(fluit_season)
            print(fluit_color)
            print(breeding_way)
            print(lux)
            print(insect)

            print(botanical_name)

        except:
            break
        else:
            print(f"==================================================================================")
            print(f"*********** {i} page {j+1} 번째 conetent 끝 ***********")
            print("==================================================================================")
            # print(f"{i}::::::::::{content_number}")

# driver = webdriver.Chrome()
# driver.get("http://api.nongsaro.go.kr/sample/ajax/garden/gardenList.html")
#
# SCROLL_PAUSE_TIME = 1
# # Get scroll height
# last_height = driver.execute_script("return document.body.scrollHeight")
# while True:
#     # Scroll down to bottom
#     for i in range(2, 23):
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         # Wait to load page
#         time.sleep(SCROLL_PAUSE_TIME)
#         # Calculate new scroll height and compare with last scroll height
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             print("진입" + str(i))
#             try:
#                 driver.find_element_by_css_selector(
#                     "# nongsaroApiLoadingAreaResult > div > div > div.pagination > strong > a:nth-child(" + str(i) + ")").click()
#                 test = driver.find_element_by_css_selector(
#                     "# nongsaroApiLoadingAreaResult > div > div > div.pagination > strong > a:nth-child(" + str(i) + ")")
#                 print(test)
#             except:
#                 break
#         last_height = new_height
#
# # images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
# count = 1
#
# time.sleep(10)
