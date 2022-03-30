# < 1. 장고 내부명령어로 생성된 앱이 아닐때 또는 패키지가 아닐때 앱에서 모델을 불러와서 DB에 접근할때 위치를 제대로 못찾을 때가 있음
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

# 1. > 이럴때는 os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")와 django.setup을 하고 실행하면 작동함
# 해당 내용은 settings.py에도 있는 내용이지만 경로를 찾지 못하기에 직접 여기서 실행할 수 있게 함

# time.sleep() 함수를 사용준비
import time

# pymysql을 이용해서 sql query문을 사용준비
import pymysql
import requests

# bs4를 이용 html 문서 내용을 태그 기준으로 찾을 준비
from bs4 import BeautifulSoup

from config.my_settings import MY_DATABASES
from plant.models import *

# < 2. pymysql을 이용하여 DB에 접근, sql query문을 사용하는 부분
db = pymysql.connect(
    host=MY_DATABASES["default"]["HOST"],
    port=3306,
    user=MY_DATABASES["default"]["USER"],
    passwd=MY_DATABASES["default"]["PASSWORD"],
    db=MY_DATABASES["default"]["NAME"],
    charset="utf8mb4",
)

# db.cursor()로 위치커서를 잡아주고 execute()를 이용하여 sql query문을 보내줌
# 실행후에는 .commit()하지 않으면 반영되지 않음.직접 cosole에서 할때도 commit해야하는 것과 같음
cursor = db.cursor()
cursor.execute("DELETE FROM plant_plant;")
db.commit()
time.sleep(2)
# db.close() 하지 않으면 밑에서 orm이 작동하지 않음. db 접근이 중복으로 되어 생기는 문제로 생각됨.
db.close()
time.sleep(3)

# 2. > sql query문을 이용하여 table의 내용을 비우고 시작

# id = 0

for i in range(1, 23):
    #####################################################################
    # bs4 사용법 요약

    # from bs4 import BeautifulSoup
    # html = """<html><head></head><body>test data</body></html> """
    # soup = BeautifulSoup(html, 'html.parser')
    # print(soup.select_one('body').text)
    #####################################################################

    print(f"========================= {i}:page 시작 =========================")
    url = f"http://api.nongsaro.go.kr/sample/ajax/ajax_local_callback.jsp?garden/gardenList?apiKey=nongsaroSampleKey&htmlArea=nongsaroApiLoadingAreaResult&pageNo={i}&serviceType=ajaxType"
    # url = f"http://api.nongsaro.go.kr/service/ajax/ajax_local_callback.jsp?garden/gardenList?apiKey=20220310B12R88R0WTCQTCD4DYSJ7W&htmlArea=nongsaroApiLoadingAreaResult&pageNo={i}&serviceType=ajaxType"

    html_txt = requests.get(url).text
    soup = BeautifulSoup(html_txt, "html.parser")

    # print(html_txt)

    for j in range(10):
        try:
            # 웹사이트의 검색페이지에서 식물별 상세페이지의 경로를 추출, 이곳에서 사용한 image도 같이 추출
            image = soup.select("img")[j]["src"]

            main_name = soup.select(".nTitle")[j].text
            print(main_name)

            tr = soup.select("td > a")[j]["onclick"]
            tr = tr.lstrip("fncDtl(")
            tr = tr.strip().rstrip("eslaf nruter ;)")
            content_number = tr.replace("'", "")

            # 위에서 알아낸 상세페이지의 경로를 이용하여 상세페이지 url을 통하여 밑의 정보 추출
            url = f"http://api.nongsaro.go.kr/sample/ajax/ajax_local_callback.jsp?garden/gardenDtl?apiKey=nongsaroSampleKey&htmlArea=nongsaroApiLoadingAreaResult&pageNo={i}&cntntsNo={content_number}&serviceType=ajaxType"
            # url = f"http://api.nongsaro.go.kr/service/ajax/ajax_local_callback.jsp?garden/gardenDtl?apiKey=20220310B12R88R0WTCQTCD4DYSJ7W&htmlArea=nongsaroApiLoadingAreaResult&pageNo={i}&cntntsNo={content_number}&serviceType=ajaxType"

            content_html = requests.get(url).text

            content = BeautifulSoup(content_html, "html.parser")

            botanical_name = content.select("tr > td")[0].text
            english_name = content.select("tr > td")[1].text
            general_name = content.select("tr > td")[2].text
            type_name = content.select("tr > td")[3].text
            origin = content.select("tr > td")[4].text
            advise_info = content.select("tr > td")[5].text
            image_link = content.select("tr > td")[6].text

            height_info = content.select("tr > td")[7].text
            if height_info == "":
                height_info = 0
            else:
                pass
            width_info = content.select("tr > td")[8].text
            if width_info == "":
                width_info = 0
            else:
                pass
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
            height_big = content.select("tr > td")[37].text
            height_mid = content.select("tr > td")[38].text
            height_small = content.select("tr > td")[39].text

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
            print(f"*********** {i} page {j + 1} 번째 conetent 시작 ***********")
            print(main_name)
            print(image)

            print(botanical_name)
            print(english_name)
            print(general_name)
            print(type_name)
            print(origin)
            print(advise_info)
            print(image_link)
            print(height_info)
            print(width_info)
            print(leaftype_info)

            # print(smell_info)
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
            # print(potsize_big)
            # print(potsize_mid)
            #
            # print(potsize_small)
            # print(width_big)
            # print(width_mid)
            # print(width_small)
            # print(length_big)
            # print(length_mid)
            # print(length_small)
            # print(height_big)
            # print(height_mid)
            # print(height_small)
            #
            # print(volume_big)
            # print(volume_mid)
            # print(volume_small)
            # print(price_big)
            # print(price_mid)
            # print(price_small)
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
            print(location)

            # print(insect)

        except:
            continue
        else:
            id = (i - 1) * 10 + j + 1
            # plant_category_id를 foreign key로 참조하기 때문에 해당 키를 이용하여 plant_category_id 설정
            # 나머지 변수들도 Plant 클래속의 변수로 넣어주고 객체를 완성
            try:
                plant_category_id = PlantCategory.objects.get(category=type_name)
            except:
                plant_category_id = PlantCategory.objects.get(id=1)
            else:
                pass

            pt = Plant(
                plant_category_id=plant_category_id,
                id=id,
                # updated_at=datetime.now(),
                # created_at=datetime.now(),
                main_name=main_name,
                image=image,
                botanical_name=botanical_name,
                english_name=english_name,
                general_name=general_name,
                type_name=type_name,
                origin=origin,
                advise_info=advise_info,
                image_link=image_link,
                height_info=int(height_info),
                width_info=int(width_info),
                leaftype_info=leaftype_info,
                toxic_info=toxic_info,
                breeding_info=breeding_info,
                extraperiod_info=extraperiod_info,
                grow_level=grow_level,
                growth_speed=growth_speed,
                growth_temp=growth_temp,
                lowest_temp=lowest_temp,
                humidity=humidity,
                fertilizer_info=fertilizer_info,
                soil_info=soil_info,
                water_spring=water_spring,
                water_summer=water_summer,
                water_fall=water_fall,
                water_winter=water_winter,
                insect_info=insect_info,
                extragrow_info=extragrow_info,
                functional_info=functional_info,
                care_need=care_need,
                type=type,
                growth_type=growth_type,
                indoor_garden=indoor_garden,
                ecology=ecology,
                leaf_pattern=leaf_pattern,
                leaf_color=leaf_color,
                flower_season=flower_season,
                flower_color=flower_color,
                fluit_season=fluit_season,
                fluit_color=fluit_color,
                breeding_way=breeding_way,
                lux=lux,
                location=location,
            )

            # pt.save() 통해 새 객체를 database에 insert
            pt.save()
            print(f"==================================================================================")
            print(f"*********** {i} page {j + 1} 번째 conetent 끝 ***********")
            print("==================================================================================")

            time.sleep(1)
