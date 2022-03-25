from django.core.files.uploadedfile import UploadedFile
from user.models import UserImg


# update user image 함수
def update_user_image(user_id: int, img_file: UploadedFile):
    # 기존 data 존재 한다면 update
    if UserImg.objects.get(user_id=user_id):
        return UserImg.objects.update(img=img_file)
    # 기존 data 없다면 create
    else:
        return UserImg.objects.create(user_id=user_id, img=img_file)
