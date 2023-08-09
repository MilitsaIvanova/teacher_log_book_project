from django.contrib import admin
from my_diary.account_app.models import  TeachersSubject, DiaryUser
@admin.register(DiaryUser)
class DiaryUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions',)

@admin.register(TeachersSubject)
class SubjectAdmin(admin.ModelAdmin):
    pass





