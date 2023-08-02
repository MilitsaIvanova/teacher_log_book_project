from django.urls import include,path
from my_diary.event_app.views import my_calendar,all_events,EventCreateView,EventEditView,remove

urlpatterns=[
    path('calendar/',my_calendar,name='calendar'),
    path('all_events/',all_events,name='all_events'),
    path('add_event/',EventCreateView.as_view(),name='add_event'),
    path('update/<int:pk>',EventEditView.as_view(),name='calendar update'),
    path('remove',remove,name='remove'),
]