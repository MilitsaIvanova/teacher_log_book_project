
from django import forms
from django.forms import DateTimeInput

from my_diary.event_app.models import Event
from my_diary.students_and_groups.models import Student, Group


class CreateEventForm(forms.ModelForm):
    lesson_with = forms.ModelChoiceField(
        queryset=Student.objects.none(),
        required=False,
        empty_label='Select Student',

    )
    lesson_with_group = forms.ModelChoiceField(
        queryset=Group.objects.none(),
        required=False,
        empty_label='Select Group',
    )
    class Meta():
        model=Event
        fields=('name','start','end','lesson_with','lesson_with_group')
        widgets = {
            'start': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end': DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    def __init__(self,*args,**kwargs):
        user=kwargs.pop('user',None)
        super(CreateEventForm,self).__init__(*args,**kwargs)
        if user:
            self.fields['lesson_with'].queryset=Student.objects.filter(teacher=user)
            self.fields['lesson_with_group'].queryset = Group.objects.filter(teacher=user)

class EditEventForm(forms.ModelForm):
    lesson_with = forms.ModelChoiceField(
        queryset=Student.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Select Student'
    )
    lesson_with_group = forms.ModelChoiceField(
        queryset=Group.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Select Group'
    )
    class Meta():
        model=Event
        fields=('name','start','end','lesson_with','lesson_with_group')
        widgets = {
            'start': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end': DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    def __init__(self,*args,**kwargs):
        user=kwargs.pop('user',None)
        super(EditEventForm,self).__init__(*args,**kwargs)
        if user:
            self.fields['lesson_with'].queryset=Student.objects.filter(teacher=user)
            self.fields['lesson_with_group'].queryset = Group.objects.filter(teacher=user)