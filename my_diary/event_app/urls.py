from django.urls import include,path
from my_diary.event_app.views import my_calendar,all_events,EventCreateView,EventEditView,EventDelete

urlpatterns=[
    path('calendar/',my_calendar,name='calendar'),
    path('all_events/',all_events,name='all_events'),
    path('add_event/',EventCreateView.as_view(),name='add_event'),
    path('update/<int:pk>',EventEditView.as_view(),name='calendar update'),
path('delete_event/<int:pk>',EventDelete.as_view(),name='delete event'),

]