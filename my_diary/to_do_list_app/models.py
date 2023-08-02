from django.db import models

from my_diary.account_app.models import DiaryUser


class Task(models.Model):
    title = models.CharField(max_length=30, blank=False, null=False)
    description = models.TextField(max_length=150, blank=True, null=True)
    teacher = models.ForeignKey(to=DiaryUser, on_delete=models.CASCADE)
    is_completed=models.BooleanField(default=False)