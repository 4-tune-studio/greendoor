from typing import Any

from django.core.files.uploadedfile import UploadedFile

from user.models import UserImg, Users


# upload user image // S3 upload 함수
def update_user_image(img_file: UploadedFile) -> Any:
    return UserImg.objects.create(img=img_file).img.url.split("?")[0]


# update user image url 함수
def update_user_image_url(user_id: int, img_url: str) -> str:
    Users.objects.filter(id=user_id).update(image=img_url)
    return Users.objects.get(id=user_id).image
