from django.contrib import admin

from my_diary.event_app.models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

