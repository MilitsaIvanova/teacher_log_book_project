from django.core import exceptions
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
def validate_phone_number(value):
    for ch in value:
        if not ch.isnumeric():
            raise exceptions.ValidationError('The phone number field should contain only numbers')

class DiaryUser(AbstractUser):
    email=models.EmailField(unique=True)
    first_name = models.CharField(max_length=30,blank=False,null=False)
    last_name = models.CharField(max_length=30,blank=False,null=False)
    profile_picture=models.URLField(blank=True,null=True)
    phone=models.CharField(max_length=15, null=True,blank=True, validators=(validate_phone_number,))
    state=models.CharField(max_length=20, null=True,blank=True)
    education=models.TextField(max_length=150, null=True,blank=True)
    country=models.CharField(max_length=20,null=True,blank=True)
    experience=models.TextField(max_length=200,null=True,blank=True)
    additional_details=models.TextField(max_length=300,null=True,blank=True)

class TeachersSubject(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    code = models.CharField(max_length=10)
    description = models.TextField()
    teacher=models.ForeignKey(to=DiaryUser,on_delete=models.CASCADE)
    def __str__(self):
        return self.name


