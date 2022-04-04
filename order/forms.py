from django import forms

from .models import Order
from user.models import Users


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["user_name", "email", "address", "postal_code"]
        CheckboxInput = forms.BooleanField()

        # if document.getElementById(id) == true:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["user_name"].label = "이름(배송 받으실 분)"
        self.fields["email"].label = "이메일"
        self.fields["address"].label = "배송 주소"
        self.fields["postal_code"].label = "우편 번호"


        self.fields['user_name'].widget.attrs['placeholder'] = ' 필수 입력 사항 입니다.'
        self.fields['email'].widget.attrs['placeholder'] = ' 필수 입력 사항 입니다.'
        self.fields['address'].widget.attrs['placeholder'] = ' 필수 입력 사항 입니다.'
        self.fields['postal_code'].widget.attrs['placeholder'] = ' 필수 입력 사항 입니다.'

        self.fields['user_name'].widget.attrs['value'] = Users.username
        # self.fields["user_name"].value = "이름(배송 받으실 분)"
        # self.fields["email"].value = "우편 번호"
        # self.fields["address"].value = "배송 주소"
        # self.fields["postal_code"].value = "전화 번호"


    # elif CheckboxInput == 0:
    #     def __init__(self, *args, **kwargs):
    #         super().__init__(*args, **kwargs)
    #
    #         self.fields["user_name"].label = "이(배송 받으실 분)"
    #         self.fields["email"].label = "우편 호"
    #         self.fields["address"].label = "배 주소"
    #         self.fields["postal_code"].label = "전 번호"
