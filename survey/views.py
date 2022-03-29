from django.shortcuts import render
from survey.models import Survey, Answer
from django.views.decorators.csrf import csrf_protect

# Create your views here.

def home(request):
    print("list 모듈 동작!")
    # filter 조건절에 해당
    # [0] 레코드중에서 첫번째 요청
    # select * from survey_survey where status='y' => row 10
    # 최신 데이터 1개만 추출 / 내림차순 : order by('-xx')[index]
    survey = Survey.objects.filter(status='y').order_by('-survey_idx')[0]

    return render(request, "survey/list_test.html", {'survey': survey})


#-----------------------------------------------------------------------------


@csrf_protect
def save_survey(request):
    # 문제 번호와 응답번호를 Answer 객체에 저장한다.
    survey_idx = request.POST["survey_idx"]
    print("Type : ", type(survey_idx))
    # survey_survey primary key -> 1:n 질문에 대한 답변의 값(survey)
    # num :선택한 설문의 항목 번호
    dto = Answer(survey_idx=int(request.POST["survey_idx"]), num=request.POST["num"])
    # insert query 가 호출
    dto.save()

    return render(request, "survey/success.html", {'survey_idx': survey_idx})


#-------------------------------------------------------------------------------


@csrf_protect
def show_result(request):
    # 문제 번호
    idx = request.GET["survey_idx"]

    # select * from survey where survey_idx=1 과 같다.
    ans = Survey.objects.get(survey_idx=idx)

    # 각 문항에 대한 값으로 리스트를 만들어 놓는다.
    answer = [ans.ans1, ans.ans2, ans.ans3, ans.ans4]

    # Survey.objects.raw("""SQL문""")
    surveyList = Survey.objects.raw("""
        SELECT survey_idx, num, count(num) sum_num FROM survey_answer
            WHERE survey_idx=%s
            GROUP BY survey_idx,num
            ORDER BY num
        """, params=idx)

    surveyList = zip(surveyList, answer)

    return render(request, "survey/result.html", {'surveyList': surveyList})


# write.html 연결
def write(request):
    return render(request, "survey/write.html")


# write에 받은거 DB 연동
def insert(request):
    # 데이터 베이스에 입력 처리 (idx 는 Oracle의 순번과 동일)
    addq = Survey(question=request.POST['question'],
                  ans1=request.POST['ans1'],
                  ans2=request.POST['ans2'],
                  ans3=request.POST['ans3'],
                  ans4=request.POST['ans4'],
                  status=request.POST['status'],
                  )
    addq.save()
    return redirect("/survey/list")

#질문목록 정의 / 갯수
def list(request):
    items = Survey.objects.order_by('survey_idx')

    # group 함수
    survey_count = Survey.objects.all().count()

    # 이제 이 값을 urls에 넘겨줘야지.
    return render(request, "survey/survey_list.html", {'items': items, 'survey_count': survey_count})

# 상세페이지
def detail(request):
    idv = request.GET['survey_idx']
    # select * from address_address where idx = idv
    addq = Survey.objects.get(survey_idx=idv)
    return render(request, 'survey/detail.html', {'addq': addq})

# 삭제 기능
# csrf_protect는 csrf 방식을 검증한다.
# 앞으로 post 방식일 때는 반드시 사용을 원칙으로 한다.
@csrf_protect
def delete(request):
    idv = request.POST['survey_idx']
    print("survey_idx:", idv)
    # delete * from address_address where idx = idv
    # 선택한 데이터의 레코드가 삭제됨
    addq = Survey.objects.get(survey_idx=idv).delete()
    return redirect('/survey/list')

# =====================================================
# 수정 기능
@csrf_protect
def update(request):
    idv = request.POST['survey_idx']
    question = request.POST['question']
    ans1 = request.POST['ans1']
    ans2 = request.POST['ans2']
    ans3 = request.POST['ans3']
    ans4 = request.POST['ans4']
    status = request.POST['status']

    print("survey_idx:", idv)
    print("question:", question)
    print("ans1:", ans1)
    print("ans2:", ans2)
    print("ans3:", ans3)
    print("ans4:", ans4)
    print("status:", status)

    # 수정 데이터 베이스 처리(idx=id -> 값을 넣으면 수정, 없으면 auto로 생성되므로 없어도됨)
    addq = Survey(survey_idx=idv, question=question, ans1=ans1, ans2=ans2, ans3=ans3, ans4=ans4, status=status)

    # 데이터 레코드가 수정됨
    addq.save()

    return redirect('/survey/list')