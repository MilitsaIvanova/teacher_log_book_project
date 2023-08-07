from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.forms import  TimeInput

from my_diary.account_app.models import DiaryUser,Student,Group

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

class DiaryUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model=DiaryUser
        fields=('username', 'email','first_name','last_name')

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,"placeholder":"Username"}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete":"current-password","placeholder":"Password"}),
    )

class ProfileEditForm(forms.ModelForm):
    class Meta():
        model=DiaryUser
        fields=('email','first_name','last_name','profile_picture','phone','state','education','country','experience','additional_details')
        exclude=('password','username','subjects')
        labels={
            'email':'Email',
            'first_name':'First Name',
            'last_name':'Last Name',
            'profile_picture':'Profile Picture',
            'phone': 'Phone',
            'state':'State',
            'education':'Education',
            'country':'Country',
            'experience':'Experience',
            'additional_details':'Additional details'
        }
class AddStudentForm(forms.ModelForm):
    class Meta():
        model=Student
        fields=('name','email','contact_number','place','lesson_time','more_information')
        widgets = {
            'lesson_time': TimeInput(attrs={'type': 'time'}),
        }

class EditStudentForm(forms.ModelForm):
    class Meta():
        model=Student
        fields=('name','email','contact_number','place','lesson_time','more_information')
        widgets = {
            'lesson_time': TimeInput(attrs={'type': 'time'}),
        }


class GroupCreateForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = Group
        fields = ('name', 'year', 'students','place','lesson_time')
        exclude = ('teacher',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(GroupCreateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['students'].queryset = Student.objects.filter(teacher=user)
class EditGroupForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta():
        model=Group
        fields=('name','year','students','place','lesson_time')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EditGroupForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['students'].queryset = Student.objects.filter(teacher=user)