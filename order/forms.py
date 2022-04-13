from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["user_name", "email", "address", "postal_code"]
        CheckboxInput = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["user_name"].label = "이름(배송 받으실 분)"
        self.fields["email"].label = "이메일"
        self.fields["address"].label = "배송 주소"
        self.fields["postal_code"].label = "우편 번호"

        self.fields["user_name"].widget.attrs["placeholder"] = " 필수 입력 사항 입니다."
        self.fields["email"].widget.attrs["placeholder"] = " 필수 입력 사항 입니다."
        self.fields["address"].widget.attrs["placeholder"] = " 필수 입력 사항 입니다."
        self.fields["postal_code"].widget.attrs["placeholder"] = " 필수 입력 사항 입니다."
