from django.db import models
from config.models import BaseModel


# Create your models here.

# class Level(models.Model):
#     name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name



class Question(BaseModel):
    number = models.IntegerField(unique=True)
    content = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.number} - {self.content}"


class Choice(BaseModel):
    content = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    question = models.ForeignKey(to="survey.Question", on_delete=models.CASCADE)
    # level = models.ForeignKey(to="survey.Level", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content
