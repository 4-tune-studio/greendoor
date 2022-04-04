from django import forms

from .models import Order
from user.models import Users

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["user_name", "email", "address", "postal_code", "city"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["user_name"].label = "이름(배송 받으실 분)"
        self.fields["email"].label = "우편 번호"
        self.fields["address"].label = "배송 주소"
        self.fields["postal_code"].label = "전화 번호"