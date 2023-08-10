from django.contrib import admin

from my_diary.to_do_list_app.models import Task


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title','teacher','is_completed']
    list_filter = ['is_completed']
    search_fields = ['title', 'teacher']