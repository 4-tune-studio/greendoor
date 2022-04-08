const makeSpinner = () => {
        const spinner = document.createElement('div');
        const spinnerImage = document.createElement('img');
        spinner.classList.add('loading');
        spinnerImage.setAttribute('src', '/static/img/spinner.gif');
        spinnerImage.classList.add('spinner');
        spinner.appendChild(spinnerImage);
        return spinner;
    };

const list = document.querySelector('.list');
const spinner = makeSpinner();

const addSkeleton = () => {
    const skeleton = document.querySelector('.skeleton');
    skeleton.setAttribute('id', 'skeleton-on');
};

const removeSkeleton = () => {
    const skeleton = document.querySelector('.skeleton');
    skeleton.setAttribute('id', 'skeleton-off');
};


const loadingStart = () => {
    addSkeleton();
    list.appendChild(spinner);
};

const loadingFinish = () => {
    removeSkeleton();
    list.removeChild(spinner);
};

// 비 동기식 으로,,,
function addNewContent() {
    $.ajax({
        type: "GET", // request 전달 방식 (POST, GET 등)
        url: newFeedURl,
        headers: {//헤더에 csrf 토큰 추가
                'X-CSRFToken': csrf
            },
        data: {// json 형식으로 서버에 데이터 전달
            "page": page // page 번호를 서버에 전달 // 따로 인자로 page를 받지 않아도 증감 연산된 page가 자동으로 할당되는지 여부 확인
        },
        dataType: "json", // json 형식으로 데이터 주고 받기
        success: function (result) {
          const data = JSON.parse(result)
          // data 반복문으로 태그 넣기
          for (let i = 0; i < data.length; i++) {
              let rowData = data[i];
              const appendNode = `<a href="/feed/${rowData.pk}"><img class="image" src="${rowData.fields.image}"></a>`;
              $("#new-feed-img").append(appendNode);
          }
          // 가져온 데이터가 18개 이면 더 가져올 데이터가 있다고 판단 다시 관찰 시작
          // 18개가 아닐경우 더이상 가져올 데이터가 없다고 판단 관찰 중지상태로 끝내기
          if (data.length === 18) {
              observer.observe(sentinel);
          }
        },
        error: function (request, status, error) {
          console.log(`request: ${request}`);
          console.log(`request: ${status}`);
          console.log(`request: ${error}`);
        },
        beforeSend: function () { // ajax 보내기 전
            loadingStart();
            console.log("페이지 스크롤 시작");
            // 통신 시작할 때 관찰 끄기
            observer.unobserve(sentinel);
        },
        complete: function () { // ajax 완료
            loadingFinish();
            console.log("페이지 스크롤 끝");
        }
    });
}



// target 선언
const sentinel = document.querySelector("#sentinel");

// option 설정
const option = {
    root: null, //viewport
    rootMargin: "0px",
    threshold: 1, // 전체(100%)가 viewport에 들어와야 callback함수 실행
};

// callback 함수 정의
const callback = (entries, observer) => {
    entries.forEach(entry => {
        if(entry.isIntersecting) {
            page ++; // 2부터 시작
            //console.log(page);
            addNewContent();
        }
    });
};

// IntersectionsObserver 생성
const observer = new IntersectionObserver(callback, option);

// target 관찰
observer.observe(sentinel);