from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm


# get_user_model
# 프로젝트에서 활성화 된 사용자 모델을 반환해 준다

# UserChangeForm
# 사용자의 정보 및 권한을 변경하기 위해 admin 인터스페이스에서 사용되는 ModelForm
# 일반 사용자가 접근 해서는 안될 정보들(fields)까지 모두 수정이 가능
# 따라서 UserChangeForm 상속 받아 user 모델에서 접근 가능한 것만 지정해 준다
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ["zipcode", "address", "phonenumber"]
