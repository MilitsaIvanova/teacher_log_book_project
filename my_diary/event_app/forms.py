
from django import forms

from my_diary.event_app.models import Event


class EditEventForm(forms.ModelForm):
    class Meta():
        model=Event
        fields=('name','start','end')