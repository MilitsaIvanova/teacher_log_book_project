from django.contrib import admin

from my_diary.students_and_groups.models import Student, Group


# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass
