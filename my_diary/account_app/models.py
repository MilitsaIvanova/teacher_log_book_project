from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class DiaryUser(AbstractUser):
    email=models.EmailField(unique=True)
    first_name = models.CharField(max_length=30,blank=False,null=False)
    last_name = models.CharField(max_length=30,blank=False,null=False)
    profile_picture=models.URLField(blank=True,null=True)
    phone=models.CharField(max_length=15, null=True,blank=True)
    state=models.CharField(max_length=20, null=True,blank=True)
    education=models.TextField(max_length=150, null=True,blank=True)
    country=models.CharField(max_length=20,null=True,blank=True)
    experience=models.TextField(max_length=200,null=True,blank=True)
    additional_details=models.TextField(max_length=300,null=True,blank=True)

class TeachersSubject(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    teacher=models.ForeignKey(to=DiaryUser,on_delete=models.CASCADE)
class Student(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    contact_number = models.CharField(max_length=10, blank=True, null=True)
    teacher=models.ForeignKey(to=DiaryUser,on_delete=models.CASCADE)
    place=models.CharField(max_length=50,null=True,blank=True)
    lesson_time=models.TimeField(null=True,blank=True)
    more_information=models.TextField(max_length=500, blank=True,null=True)

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
