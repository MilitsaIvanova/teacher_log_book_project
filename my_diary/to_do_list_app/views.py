from django.http import request, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, DeleteView

from my_diary.account_app.models import DiaryUser
from my_diary.to_do_list_app import models


# Create your views here.
class TaskCreateView(CreateView):
    fields = ['title', 'description']
    model = models.Task
    template_name = 'create_task.html'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.teacher_id = self.request.user.id
        task.save()
        return redirect('/dashboard/'+str(self.request.user.pk))


class TaskList(DetailView):
    template_name = 'dashboard.html'
    model = DiaryUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.request.user.task_set.all()
        return context


class TaskDeleteView(DeleteView):
    model = models.Task
    template_name = 'task_delete_confirmation.html'

    def get_success_url(self):
        return reverse_lazy('dashboard', kwargs={
            'pk': self.request.user.pk
        })


class TaskDetailView(DetailView):
    model = models.Task
    template_name = 'task_detail.html'


class ToggleTaskCompletionView(View):
    def post(self, request, task_id):
        try:
            task = models.Task.objects.get(pk=task_id)
            task.is_completed = not task.is_completed
            task.save()
            return JsonResponse({'status': 'success', 'is_completed': task.is_completed})
        except models.Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
