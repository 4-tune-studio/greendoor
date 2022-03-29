from django.db import models

# 설문조사 문항
class Survey(models.Model):
    # 설문 인덱스
    survey_idx = models.AutoField(primary_key=True)

    # 설문 문제
    question = models.TextField(null=True)

    # 답 1~3
    ans1 = models.TextField(null=True)
    ans2 = models.TextField(null=True)
    ans3 = models.TextField(null=True)
    ans4 = models.TextField(null=True)


    # 설문진행상태(y=진행중, n=종료)
    status = models.CharField(max_length=1, default="y")


# ------------------------------------------------------------
class Answer(models.Model):
    # 응답 아이디(자동필드 증가)
    answer_idx = models.AutoField(primary_key=True)

    # 설문 아이디
    survey_idx = models.IntegerField()

    # 응답 번호
    num = models.IntegerField()