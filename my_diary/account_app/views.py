from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from my_diary.account_app.forms import DiaryUserCreateForm, LoginForm, ProfileEditForm

from my_diary.account_app.models import DiaryUser, TeachersSubject
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from my_diary.event_app.views import event_counter

UserModel=get_user_model()

def about_view(request):
    return render(request, 'about_page.html')
class UserRegisterView(views.CreateView):
    model = UserModel
    form_class=DiaryUserCreateForm
    template_name = 'profile/register-page.html'
    success_url = reverse_lazy('login')

class UserLoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'profile/login-page.html'
    def get_success_url(self):
        return reverse_lazy('index')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid login credentials. Please try again.')
        return super().form_invalid(form)

class UserLogoutView(LoginRequiredMixin,auth_views.LogoutView):
    next_page = reverse_lazy('index')

@login_required
def logout_confirm(request):
    return render(request, 'profile/logout_confirmation.html')

class ProfileEditView(LoginRequiredMixin,views.UpdateView):
    login_url = 'login'

    model = UserModel
    form_class = ProfileEditForm
    template_name = 'profile/profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('profile',kwargs={
            'pk':self.object.pk
        })

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValidationError as e:
            error_message = str(e)
            context = self.get_context_data(form=form, error_message=error_message)
            return self.render_to_response(context)
class UserDeleteView(LoginRequiredMixin,views.DeleteView):
    model = UserModel
    template_name = 'profile/delete_profile.html'

    def get_success_url(self):
        return reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)



@login_required
def index(request):
    return render(request, 'index.html')


class ProfileDetails(LoginRequiredMixin,views.DetailView):
    template_name = 'profile/my_profile.html'
    model = UserModel

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['students_count']=self.request.user.student_set.count()
        context['event_count'] =event_counter(request=self.request)
        context['subjects']=TeachersSubject.objects.filter(teacher=self.request.user)
        return context

class CreateSubject(LoginRequiredMixin,views.CreateView):
    model = TeachersSubject
    template_name = 'subject/create_subject.html'
    fields = ['name','code','description']
    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('classes', kwargs={
            'pk': self.request.user.pk
        })

class EditSubject(LoginRequiredMixin,views.UpdateView):
    model = TeachersSubject
    template_name = 'subject/edit_subject.html'
    fields = ['name','code','description']
    def get_success_url(self):
        return reverse_lazy('classes', kwargs={
            'pk': self.request.user.pk
        })

class DeleteSubject(LoginRequiredMixin,views.DeleteView):
    model = TeachersSubject
    template_name = 'subject/delete_subject.html'

    def get_success_url(self):
        return reverse_lazy('classes',kwargs={
            'pk':self.request.user.pk
        })

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)



