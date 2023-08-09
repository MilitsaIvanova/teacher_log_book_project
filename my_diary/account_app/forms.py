from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField


from my_diary.account_app.models import DiaryUser

from django import forms


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





