from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.shortcuts import render, redirect

from my_diary.account_app.models import DiaryUser, TeachersSubject
from my_diary.students_and_groups.forms import AddStudentForm, EditStudentForm, GroupCreateForm, EditGroupForm
from my_diary.students_and_groups.models import Student, Group

UserModel=get_user_model()
class ClassDetails(LoginRequiredMixin,views.DetailView):
    template_name = 'students and groups/my_classes.html'
    model = UserModel
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['students']=self.request.user.student_set.all()

        return context

class GroupDetails(LoginRequiredMixin,views.DetailView):
    template_name = 'students and groups/groups.html'
    model = UserModel
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['groups']=self.request.user.group_set.all()
        return context





@login_required
def add_student(request):
    subjects_exist=TeachersSubject.objects.filter(teacher=request.user).exists()
    if request.method=="POST":
        form=AddStudentForm(request.POST,user=request.user)
        try:
            if form.is_valid():
                student = form.save(commit=False)
                student.user = request.user
                student.teacher_id = student.user.id
                student.save()
                redirect_link = '/classes/' + str(request.user.pk)
                return redirect(redirect_link)
        except ValidationError as e:

            form.add_error(None, e)

    else:
        form = AddStudentForm(user=request.user)

    context = {'form': form, 'subjects_exist': subjects_exist}
    return render(request, 'students and groups/add_student.html', context)

class EditStudent(LoginRequiredMixin,views.UpdateView):
    template_name = 'students and groups/edit_student.html'
    model = Student
    form_class = EditStudentForm
    def get_form_kwargs(self):
        kwargs = super(EditStudent, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subjects_exist = TeachersSubject.objects.filter(teacher=self.request.user.pk).exists()
        context['subjects_exist'] = subjects_exist
        return context

    def get_success_url(self):
        return reverse_lazy('classes',kwargs={
            'pk':self.request.user.pk
        })

class CreateGroup(LoginRequiredMixin,views.CreateView):
    template_name = 'students and groups/create_group.html'
    model = Group
    form_class = GroupCreateForm

    def get_form_kwargs(self):
        kwargs = super(CreateGroup, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subjects_exist = TeachersSubject.objects.filter(teacher=self.request.user.pk).exists()
        context['subjects_exist'] = subjects_exist
        students=Student.objects.filter(teacher=self.request.user.pk)
        if not students:
            context['students_in_group']=None
        else:
            context['students_in_group']=not None

        return context

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('groups', kwargs={
            'pk': self.request.user.pk
        })
class EditGroup(LoginRequiredMixin,views.UpdateView):
    template_name = 'students and groups/edit_group.html'
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
        students_exist=Student.objects.filter(teacher=self.request.user.pk).exists()
        context['students_exist']=students_exist
        subjects_exist = TeachersSubject.objects.filter(teacher=self.request.user.pk).exists()
        context['subjects_exist'] = subjects_exist
        return context
    def get_form_kwargs(self):
        kwargs = super(EditGroup, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    def get_success_url(self):
        return reverse_lazy('groups',kwargs={
            'pk':self.request.user.pk
        })
class GroupDeleteView(LoginRequiredMixin,views.DeleteView):
    model = Group
    template_name = 'students and groups/delete_group.html'

    def get_success_url(self):
        return reverse_lazy('groups',kwargs={
            'pk':self.request.user.pk
        })

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class DeleteStudentView(LoginRequiredMixin,views.DeleteView):
    model = Student
    template_name = 'students and groups/delete_student.html'

    def get_success_url(self):
        return reverse_lazy('classes',kwargs={
            'pk':self.request.user.pk
        })

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


