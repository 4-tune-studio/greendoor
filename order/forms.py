from django import forms

from .models import Order
from user.models import Users

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["user_name", "email", "address", "postal_code", "city"]
        fields[0].label = "이름(배송 받으실 분)"
        fields[1].label = "email"
        fields[2].label = "배송 주소"
        fields[3].label = "우편 번호"

        fields[4].label = "빠른 배송을 위해 도시를 입력해주세요"
        # fields = ["first_name", "last_name", "email", "address", "postal_code", "city"]
