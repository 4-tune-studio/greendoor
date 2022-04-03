import re
from typing import Any


# password 유효성 검사: 비번 길이, 영문 + 숫자 조합 여부, password == password2 일치 여부
def sign_up_password_validation(password: str, password2: str) -> Any:
    if not (6 < len(password) < 21):
        return "password 길이는 7~20자 입니다."
    elif re.search("[0-9]+", password) is None or re.search("[a-zA-Z]+", password) is None:
        return "password 형식은 영문,숫자 포함 7~20자 입니다."
    elif password != password2:
        return "password 확인 해 주세요!"


# nickname 유효성 검사: nickname 길이, 한글은 한글만, 영문은 영문 or 영문 + 숫자
def sign_up_nickname_validation(nickname: str) -> Any:
    if not (3 < len(nickname) < 21):
        return "nickname 길이는 3~20자 입니다."
    elif re.search("[가-힣]+", nickname) is None:
        if re.match("([A-Za-z0-9]{3,20})", nickname) is not None:
            if re.search("[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`'…》]+", nickname) is not None:
                return "nickname 영문 형식은 영문, 숫자 포함만 가능합니다."
        else:
            return "nickname 영문 형식은 영문, 숫자 포함만 가능합니다."
    elif re.search("[A-Za-z0-9]+", nickname) is None:
        if re.match("([가-힣]{3,20})", nickname) is not None:
            if re.search("[A-Za-z0-9-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`'…》]+", nickname) is not None:
                return "nickname 한글 형식은 오직 한글만 가능합니다."
        else:
            return "nickname 한글 형식은 오직 한글만 가능합니다."
