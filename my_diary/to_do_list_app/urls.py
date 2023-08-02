from django.urls import include,path
from my_diary.to_do_list_app import views

urlpatterns=[
    path('add_task/',views.TaskCreateView.as_view(),name='add task'),
    path('task/<int:pk>/',views.TaskDetailView.as_view(),name='task details'),
    path('task/delete/<int:pk>/', views.TaskDeleteView.as_view(),name='task delete'),
    path('dashboard/<int:pk>/', views.TaskList.as_view(), name='dashboard'),
    path('toggle_task_completion/<int:task_id>/', views.ToggleTaskCompletionView.as_view(), name='toggle_task_completion'),
]