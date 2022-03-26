from django.core.files.uploadedfile import UploadedFile

from user.models import UserImg, Users


# update user image // S3 upload 함수
def update_user_image(user_id: int, img_file: UploadedFile) -> object:
    # 기존 data 존재 한다면 update
    if UserImg.objects.get(user_id=user_id):
        return UserImg.objects.update(img=img_file)
    # 기존 data 없다면 create
    else:
        return UserImg.objects.create(user_id=user_id, img=img_file)


# update user image url 함수
def update_user_image_url(user_id: int, img_url: str) -> object:
    # 기존 data 존재 한다면 update
    check = Users.objects.get(id=user_id)
    if check["image"] is not None:
        return Users.objects.update(image=img_url)
    # 기존 data 없다면 create
    else:
        return Users.objects.create(id=user_id, image=img_url)
