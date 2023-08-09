from django.urls import path, include

from my_diary.students_and_groups import views

urlpatterns = [
    path('classes/<int:pk>', views.ClassDetails.as_view(), name='classes'),
    path('groups/<int:pk>', views.GroupDetails.as_view(), name='groups'),
    path('group/<int:pk>', views.GroupDeleteView.as_view(), name='group delete'),
    path('edit_group/<int:pk>', views.EditGroup.as_view(), name='edit group'),
    path('add_student/', views.add_student, name='add student'),
    path('edit_student/<int:pk>', views.EditStudent.as_view(), name='edit student'),
    path('delete_student/<int:pk>', views.DeleteStudentView.as_view(), name='delete student'),
    path('create_group/', views.CreateGroup.as_view(), name='create group'),
]
