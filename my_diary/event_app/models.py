from django.db import models

from my_diary.account_app.models import Student, DiaryUser


class Event(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    start=models.DateTimeField(null=True,blank=True)
    end=models.DateTimeField(null=True, blank=True)
    lesson_with=models.ForeignKey(to=Student, on_delete=models.CASCADE)
    teacher=models.ForeignKey(to=DiaryUser, on_delete=models.CASCADE)




