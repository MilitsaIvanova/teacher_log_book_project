from django.contrib import admin
from my_diary.account_app.models import  TeachersSubject, DiaryUser

@admin.register(DiaryUser)
class DiaryUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions',)
    list_display = ['username','first_name','last_name','email']
    list_filter = ['date_joined','last_login','is_staff','is_superuser']
    search_fields = ['first_name','email']
    fieldsets = (
        ('Personal info',
         {'fields':('username','first_name','last_name')}),
        ('Advanced options',
         {'classes':('collapse',),
          'fields':('groups','user_permissions','date_joined','last_login','is_superuser','is_staff','profile_picture','phone','state','education','country','experience','additional_details')})
    )

@admin.register(TeachersSubject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name','code','teacher']
    list_filter = ['teacher','name','code']
    search_fields = ['name','teacher']





