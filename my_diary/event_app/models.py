from django.db import models

from my_diary.account_app.models import  DiaryUser
from my_diary.students_and_groups.models import Student,Group


class Event(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    start=models.DateTimeField(null=True,blank=True)
    end=models.DateTimeField(null=True, blank=True)
    lesson_with=models.ForeignKey(to=Student, on_delete=models.CASCADE,null=True)
    lesson_with_group=models.ForeignKey(to=Group, on_delete=models.CASCADE,null=True)
    teacher=models.ForeignKey(to=DiaryUser, on_delete=models.CASCADE)




