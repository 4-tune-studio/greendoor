
//update user profile image api
function update_image_api(id) {
    let user_id = id
    let file = $('#file')[0].files[0]
    let form_data = new FormData()

    form_data.append("user_id", user_id)
    form_data.append("image", file)
    $.ajax({
        type: "POST",
        url: UserProfileUpdateURL,
        headers: Headers,
        dataType: 'json',
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            alert("성공! 이미지 수정되었습니다 : )")
            console.log(response)
        },
        error: function () {
            alert("실패! 이미지 확장자를 확인해 주세요.")
            location.reload()

        },
    })
}

//이미지 미리 보기 함수
function handleFileSelect(event) {
    var input = this;
    console.log(input.files)
    if (input.files && input.files.length) {
        var reader = new FileReader();
        this.enabled = false
        reader.onload = (function (e) {
            console.log(e)
            $("#preview").html(['<img class="thumb" style="width: 150px; height: 150px; object-fit: cover" src="', e.target.result, '" title="', escape(e.name), '"/>'].join(''))
        });
        reader.readAsDataURL(input.files[0]);
        $("#user-image").hide();
    }
}

$('#file').change(handleFileSelect);


//회원 탈퇴 함수
function delchk() {
            return confirm("정말 삭제하시겠습니까? 삭제하시면 복구할 수 없습니다");
        }
