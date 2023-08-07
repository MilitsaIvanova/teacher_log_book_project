
from django import forms
from django.forms import DateTimeInput

from my_diary.event_app.models import Event

class CreateEventForm(forms.ModelForm):
    class Meta():
        model=Event
        fields=('name','start','end')
        widgets = {
            'start': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end': DateTimeInput(attrs={'type': 'datetime-local'}),
        }
class EditEventForm(forms.ModelForm):
    class Meta():
        model=Event
        fields=('name','start','end')
        widgets = {
            'start': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end': DateTimeInput(attrs={'type': 'datetime-local'}),
        }