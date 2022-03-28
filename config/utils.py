ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif", "jfif"]


# 허용된 이미지 확장자 판단
def allowed_file(filename: str) -> bool:
    # '.'이 파일 이름안에 있고 '.' 으로 나눴을때 뒷부분이 허용된 확장자 리스트 안에 있을 때
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# 업로드 이미지 확장자 리턴
def get_file_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[1].lower()
