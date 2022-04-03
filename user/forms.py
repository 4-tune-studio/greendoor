from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

# get_user_model
# 프로젝트에서 활성화 된 사용자 모델을 반환해 준다


# UserChangeForm
# 사용자 정보 및 권한을 변경하기 위해 admin 인터스페이스에서 사용 되는 ModelForm
# 일반 사용자가 접근 해서는 안될 정보들(fields)까지 모두 수정 가능
# 때문에 UserChangeForm 상속 받아 user 모델에서 접근 가능한 것만 지정해 준다
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ["nickname", "zipcode", "address", "phonenumber"]

    def __init__(self, *args, **kwargs):
        # *args : 복수의 인자를 받고자 할 때, *뒤 변수명을 적으면 된다
        # **kwargs : 여러 키워드 파라미터를 받을 수 있다(ex- x=10 과 같은!)
        super().__init__(*args, **kwargs)
        # super()을 이용해 부모클래스의 내용을 가지고 올 수 있다.=> 오버라이딩 즉 Blogapp 내용에 접근
        self.fields['nickname'].label = "이름(배송 받으실 분)"
        self.fields['zipcode'].label = "우편 번호"
        self.fields['address'].label = "배송 주소"
        self.fields['phonenumber'].label = "전화 번호"
