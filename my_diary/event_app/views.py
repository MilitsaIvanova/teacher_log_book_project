from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from my_diary.account_app.models import Student
from my_diary.event_app.forms import EditEventForm
from my_diary.event_app.models import Event

@login_required
def my_calendar(request):
    all_events=Event.objects.filter(teacher=request.user)
    context={
        'events':all_events,
    }
    return render(request, 'my_calendar.html',context)
@login_required
def all_events(request):
    all_events=Event.objects.filter(teacher=request.user)
    out=[]
    for event in all_events:
        out.append({
            'title':event.name,
            'id':event.id,
            'start':event.start.strftime("%m/%d/%Y, %H:%M:%S"),
            'end':event.end.strftime("%m/%d/%Y, %H:%M:%S"),
        })
    return JsonResponse(out,safe=False)
# @login_required
# def add_event(request):
#     start=request.GET.get("start",None)
#     end=request.GET.get("end",None)
#     title=request.GET.get("title",None)
#     event=Event(name=str(title),start=start,end=end)
#     event.save()
#     data={}
#     return JsonResponse(data)
class EventCreateView(CreateView):
    fields = ['name','start','end']
    model = Event
    template_name = 'add_event.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        teacher_students=Student.objects.filter(teacher=self.request.user.id)
        context['students']=teacher_students
        return context


    def form_valid(self, form):
        event=form.save(commit=False)
        event.user=self.request.user
        event.teacher_id=self.request.user.id
        select_student_id=self.request.POST.get('student')
        event.lesson_with_id=select_student_id
        event.save()
        return redirect('/calendar/')


class EventEditView(UpdateView):
    template_name = 'update_event.html'
    model = Event
    form_class = EditEventForm
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        current_student=self.object.lesson_with
        teacher_students=Student.objects.filter(teacher=self.request.user.id)
        context['students']=teacher_students
        context['current_student_name']=current_student.name
        return context

    def form_valid(self, form):
        event = form.save(commit=False)
        event.user = self.request.user
        event.teacher_id = self.request.user.id
        select_student_id = self.request.POST.get('student')
        event.lesson_with_id = select_student_id
        event.save()
        return redirect('/calendar/')
# @login_required
# def update(request):
#     start=request.GET.get('start',None)
#     end = request.GET.get("end", None)
#     title = request.GET.get("title", None)
#     id=request.GET.get('id',None)
#     event=Event.objects.get(id=id)
#     event.start=start
#     event.end=end
#     event.name=title
#     event.save()
#     data={}
#     return JsonResponse(data)
@login_required
def remove(request):
    id=request.GET.get('id',None)
    event=Event.objects.get(id=id)
    event.delete()
    data={}
    return JsonResponse(data)
