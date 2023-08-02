from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from my_diary.account_app.forms import DiaryUserCreateForm,LoginForm,ProfileEditForm,AddStudentForm,EditStudentForm
from my_diary.account_app.models import DiaryUser,Student
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class UserRegisterView(views.CreateView):
    model = DiaryUser
    form_class=DiaryUserCreateForm
    template_name = 'register-page.html'
    success_url = reverse_lazy('login')

class UserLoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login-page.html'
    next_page = reverse_lazy('index')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid login credentials. Please try again.')
        return super().form_invalid(form)

class UserLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('index')

@login_required
def logout_confirm(request):
    return render(request,'logout_confirmation.html')

class ProfileEditView(LoginRequiredMixin,views.UpdateView):
    login_url = 'login'

    model = DiaryUser
    form_class = ProfileEditForm
    template_name = 'profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('profile',kwargs={
            'pk':self.object.pk
        })
class UserDeleteView(views.DeleteView):
    model = DiaryUser
    template_name = 'delete_profile.html'

    def get_success_url(self):
        return reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)



@login_required
def index(request):
    return render(request,'index.html')


class ClassDetails(views.DetailView):
    template_name = 'my_classes.html'
    model = DiaryUser
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['students']=self.request.user.student_set.all()
        return context


class ProfileDetails(views.DetailView):
    template_name = 'my_profile.html'
    model = DiaryUser
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['students_count']=self.request.user.student_set.count()
        return context
@login_required
def add_student(request):
    form=AddStudentForm(request.POST or None)
    if form.is_valid():
        student=form.save(commit=False)
        student.user=request.user
        student.teacher_id=student.user.id
        student.save()
        redirect_link='/classes/'+str(request.user.pk)
        return redirect(redirect_link)
    context={'form':form}

    return render(request,'add_student.html',context)

class EditStudent(views.UpdateView):
    template_name = 'edit_student.html'
    model = Student
    form_class = EditStudentForm

    def get_success_url(self):
        return reverse_lazy('classes',kwargs={
            'pk':self.request.user.pk
        })
