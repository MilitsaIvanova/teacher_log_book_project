from django.contrib import admin

from my_diary.students_and_groups.models import Student, Group


# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'teacher']
    list_filter = ['teacher']
    search_fields = ['name', 'teacher']

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'teacher']
    list_filter = ['year']
    search_fields = ['name', 'teacher']