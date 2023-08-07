from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from my_diary.account_app.models import Student, TeachersSubject, Group, DiaryUser
@admin.register(DiaryUser)
class DiaryUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(TeachersSubject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass



