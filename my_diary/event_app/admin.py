from django.contrib import admin

from my_diary.event_app.models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_lesson_with', 'get_lesson_with_group','teacher']
    list_filter = ['start', 'end']
    search_fields = ['name', 'teacher']

    def get_lesson_with(self, obj):
        return obj.lesson_with.name if obj.lesson_with else None

    get_lesson_with.short_description = 'Lesson With Student'

    def get_lesson_with_group(self, obj):
        return obj.lesson_with_group.name if obj.lesson_with_group else None

    get_lesson_with_group.short_description = 'Lesson With Group'

