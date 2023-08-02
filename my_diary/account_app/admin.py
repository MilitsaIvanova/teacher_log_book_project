from django.contrib import admin
from my_diary.account_app.models import Student, Subject, Group, DiaryUser


# Register your models here.



@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(DiaryUser)
class DiaryUserAdmin(admin.ModelAdmin):
    pass
