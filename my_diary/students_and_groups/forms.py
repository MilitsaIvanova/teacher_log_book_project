from django import forms
from django.forms import TimeInput

from my_diary.account_app.models import TeachersSubject
from my_diary.students_and_groups.models import Student, Group


class AddStudentForm(forms.ModelForm):
    subject=forms.ModelChoiceField(
        queryset=TeachersSubject.objects.none(),
        empty_label="Select a subject",
    )
    class Meta():
        model=Student
        fields=('name','email','contact_number','place','lesson_time','more_information','subject')
        widgets = {
            'lesson_time': TimeInput(attrs={'type': 'time'}),
        }
    def __init__(self,*args,**kwargs):
        user=kwargs.pop('user',None)
        super(AddStudentForm,self).__init__(*args,**kwargs)
        if user:
            self.fields['subject'].queryset=TeachersSubject.objects.filter(teacher=user)

class EditStudentForm(forms.ModelForm):
    subject = forms.ModelChoiceField(
        queryset=TeachersSubject.objects.none(),
        empty_label="Select a subject",
    )
    class Meta():
        model=Student
        fields=('name','email','contact_number','place','lesson_time','more_information','subject')
        widgets = {
            'lesson_time': TimeInput(attrs={'type': 'time'}),
        }
    def __init__(self,*args,**kwargs):
        user=kwargs.pop('user',None)
        super(EditStudentForm,self).__init__(*args,**kwargs)
        if user:
            self.fields['subject'].queryset=TeachersSubject.objects.filter(teacher=user)

class GroupCreateForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    subject = forms.ModelChoiceField(
        queryset=TeachersSubject.objects.none(),
        empty_label="Select a subject",
    )
    class Meta:
        model = Group
        fields = ('name', 'year', 'students','place','lesson_time','subject')
        exclude = ('teacher',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(GroupCreateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['students'].queryset = Student.objects.filter(teacher=user)
            self.fields['subject'].queryset = TeachersSubject.objects.filter(teacher=user)



class EditGroupForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    subject = forms.ModelChoiceField(
        queryset=TeachersSubject.objects.none(),
        empty_label="Select a subject",
    )
    class Meta():
        model=Group
        fields=('name','year','students','place','lesson_time','subject')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EditGroupForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['students'].queryset = Student.objects.filter(teacher=user)
            self.fields['subject'].queryset = TeachersSubject.objects.filter(teacher=user)