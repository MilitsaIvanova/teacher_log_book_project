from datetime import datetime, timedelta
from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from my_diary.students_and_groups.models import Student, Group
from my_diary.event_app.forms import EditEventForm, CreateEventForm
from my_diary.event_app.models import Event

@login_required
def my_calendar(request):
    all_events=Event.objects.filter(teacher=request.user)
    context={
        'events':all_events,
    }
    return render(request, 'events/my_calendar.html', context)
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

class EventCreateView(LoginRequiredMixin,CreateView):
    form_class = CreateEventForm
    model = Event
    template_name = 'events/add_event.html'

    def get_form_kwargs(self):
        kwargs = super(EventCreateView,self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    def form_valid(self, form):
        form.instance.teacher_id = self.request.user.id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('calendar')


class EventEditView(LoginRequiredMixin,UpdateView):
    template_name = 'events/update_event.html'
    model = Event
    form_class = EditEventForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse_lazy('calendar')
class EventDelete(LoginRequiredMixin,DeleteView):
    template_name = 'events/delete_event.html'
    model = Event

    def get_success_url(self):
        return reverse_lazy('calendar')
@login_required
def remove(request):
    id=request.GET.get('id',None)
    event=Event.objects.get(id=id)
    event.delete()
    data={}
    return JsonResponse(data)

def event_counter(request):
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday


    events_this_week = Event.objects.filter(teacher=request.user,start__range=[start_of_week, end_of_week])

    num_events = events_this_week.count()

    return num_events