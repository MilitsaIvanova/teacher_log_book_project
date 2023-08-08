from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from my_diary.account_app.forms import DiaryUserCreateForm, LoginForm, ProfileEditForm, AddStudentForm, EditStudentForm, \
    EditGroupForm, GroupCreateForm
from my_diary.account_app.models import DiaryUser, Student, Group, TeachersSubject
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from my_diary.core.access_mixin import GroupRequiredMixin
from my_diary.event_app.views import event_counter


class UserRegisterView(views.CreateView):
    model = DiaryUser
    form_class=DiaryUserCreateForm
    template_name = 'register-page.html'
    success_url = reverse_lazy('login')

class UserLoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login-page.html'
    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={
            'pk': self.request.user.pk
        })

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
class GroupDetails(views.DetailView):
    template_name = 'groups.html'
    model = DiaryUser
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['groups']=self.request.user.group_set.all()
        return context

class ProfileDetails(views.DetailView):
    template_name = 'my_profile.html'
    model = DiaryUser

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['students_count']=self.request.user.student_set.count()
        context['event_count'] =event_counter(request=self.request)
        context['subjects']=TeachersSubject.objects.filter(teacher=self.request.user)
        return context
@login_required
def add_student(request):
    if request.method=="POST":
        form=AddStudentForm(request.POST,user=request.user)
        if form.is_valid():
            student=form.save(commit=False)
            student.user=request.user
            student.teacher_id=student.user.id
            student.save()
            redirect_link='/classes/'+str(request.user.pk)
            return redirect(redirect_link)
    form=AddStudentForm(user=request.user)
    context={'form':form}

    return render(request,'add_student.html',context)

class EditStudent(LoginRequiredMixin,views.UpdateView):
    template_name = 'edit_student.html'
    model = Student
    form_class = EditStudentForm

    def get_success_url(self):
        return reverse_lazy('classes',kwargs={
            'pk':self.request.user.pk
        })
class CreateGroup(LoginRequiredMixin,views.CreateView):
    template_name = 'create_group.html'
    model = Group
    form_class = GroupCreateForm

    def get_form_kwargs(self):
        kwargs = super(CreateGroup, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('groups', kwargs={
            'pk': self.request.user.pk
        })
class EditGroup(LoginRequiredMixin,views.UpdateView):
    template_name = 'edit_group.html'
    model = Group
    form_class = EditGroupForm

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        group = Group.objects.get(pk=self.kwargs['pk'])
        context['group']=group
        if group.students:
            context['students_in_group'] = group.students.all()
        else:
            context['students_in_group']=None
        return context
    def get_form_kwargs(self):
        kwargs = super(EditGroup, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    def get_success_url(self):
        return reverse_lazy('groups',kwargs={
            'pk':self.request.user.pk
        })

class GroupDeleteView(views.DeleteView):
    model = Group
    template_name = 'delete_group.html'

    def get_success_url(self):
        return reverse_lazy('groups',kwargs={
            'pk':self.request.user.pk
        })

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class DeleteStudentView(views.DeleteView):
    model = Student
    template_name = 'delete_student.html'

    def get_success_url(self):
        return reverse_lazy('classes',kwargs={
            'pk':self.request.user.pk
        })

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class CreateSubject(views.CreateView):
    model = TeachersSubject
    template_name = 'create_subject.html'
    fields = ['name','code','description']
    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('classes', kwargs={
            'pk': self.request.user.pk
        })

class EditSubject(views.UpdateView):
    model = TeachersSubject
    template_name = 'edit_subject.html'
    fields = ['name','code','description']
    def get_success_url(self):
        return reverse_lazy('classes', kwargs={
            'pk': self.request.user.pk
        })

class DeleteSubject(views.DeleteView):
    model = TeachersSubject
    template_name = 'delete_subject.html'

    def get_success_url(self):
        return reverse_lazy('classes',kwargs={
            'pk':self.request.user.pk
        })

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)



