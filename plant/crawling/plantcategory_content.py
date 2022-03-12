# < 1. 장고 내부명령어로 생성된 앱이 아닐때 또는 패키지가 아닐때 앱에서 모델을 불러와서 DB에 접근할때 위치를 제대로 못찾을 때가 있음
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greendoor.settings")

import django

django.setup()

# 1. > 이럴때는 os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greendoor.settings")와 django.setup을 하고 실행하면 작동함
# 해당 내용은 settings.py에도 있는 내용이지만 경로를 찾지 못하기에 직접 여기서 실행할 수 있게 함

# time.sleep() 함수를 사용준비
import time

# pymysql을 이용해서 sql query문을 사용준비
import pymysql

from greendoor.my_settings import MY_DATABASES
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
cursor.execute("DELETE FROM plant_plantcategory;")
db.commit()
time.sleep(2)
# db.close() 하지 않으면 밑에서 orm이 작동하지 않음. db 접근이 중복으로 되어 생기는 문제로 생각됨.
db.close()
time.sleep(3)


# 2. > sql query문을 이용하여 table의 내용을 비우고 시작

def category_insert(category, plant_plantcategory_id):
    ptcategory = PlantCategory(id=plant_plantcategory_id,
                               category=category)
    # pt.save() 통해 새 객체를 database에 insert
    ptcategory.save()
    print(f"={plant_plantcategory_id}번 카테고리 입력완료={category}")
    plant_plantcategory_id += 1
    time.sleep(1)
    return plant_plantcategory_id


plant_plantcategory_id = 1

plant_plantcategory_id = category_insert("카테고리없음", plant_plantcategory_id)

plant_plantcategory_id = category_insert("가지과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("고란초과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("고비과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("고사리과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("괭이밥과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("국화과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("꼭두서니과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("꿀풀과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("나한송과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("난초과", plant_plantcategory_id)

plant_plantcategory_id = category_insert("노박덩굴과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("닭의장풀과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("대극과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("도금양과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("돈나무과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("돌나물과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("두릅나무과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("마디풀과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("마란타과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("마편초과", plant_plantcategory_id)

plant_plantcategory_id = category_insert("매자나무과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("면마과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("물밤나무과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("물푸레나무과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("미나리아재비과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("박주가리과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("백합과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("범의귀과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("베고니아과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("봉선화과", plant_plantcategory_id)

plant_plantcategory_id = category_insert("부처손과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("분꽃과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("뽕나무과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("사초과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("생강과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("소철과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("수선화과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("쐐기풀과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("아라우카리아과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("앵초과", plant_plantcategory_id)

plant_plantcategory_id = category_insert("야자과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("인동과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("자금우과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("장미과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("쥐꼬리망초과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("쥐손풀이과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("진달래과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("차나무과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("천남성과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("측백나무과", plant_plantcategory_id)

plant_plantcategory_id = category_insert("층층나무과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("파인애플과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("포도과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("협죽도과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("후추과", plant_plantcategory_id)

plant_plantcategory_id = category_insert("쥐손이풀과", plant_plantcategory_id)
plant_plantcategory_id = category_insert("범위귀과", plant_plantcategory_id)


