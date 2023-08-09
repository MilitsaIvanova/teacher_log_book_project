from django.core import  exceptions
from django.db import models

from my_diary.account_app.models import DiaryUser, TeachersSubject


# Create your models here.
def validate_phone_number(value):
    for ch in value:
        if not ch.isnumeric():
            raise exceptions.ValidationError('The phone number field should contain only numbers')
class Student(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    contact_number = models.CharField(max_length=10, blank=True, null=True,validators=(
        validate_phone_number,
    ))
    teacher=models.ForeignKey(to=DiaryUser,on_delete=models.CASCADE)
    place=models.CharField(max_length=50,null=True,blank=True)
    lesson_time=models.TimeField(null=True,blank=True)
    more_information=models.TextField(max_length=500, blank=True,null=True)
    subject=models.ForeignKey(to=TeachersSubject,on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)


class Group(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    teacher=models.ForeignKey(to=DiaryUser,on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name="groups",blank=True)
    place=models.CharField(max_length=50,null=True,blank=True)
    lesson_time=models.TimeField(null=True,blank=True)
    subject = models.ForeignKey(to=TeachersSubject, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name
