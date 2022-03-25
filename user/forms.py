from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm


# UserChangeForm 상속 받아 user 모델에서 접근 가능한 것만 작성해 준다
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ["nickname", "zipcode", "address", "phonenumber"]
