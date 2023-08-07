from django.urls import include, path

from my_diary.account_app import views
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name='index.html'), name='index'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('logout/yes/', views.UserLogoutView.as_view(), name="logout"),
    path('classes/<int:pk>', views.ClassDetails.as_view(), name='classes'),
    path('groups/<int:pk>', views.GroupDetails.as_view(), name='groups'),
    path('group/<int:pk>', views.GroupDeleteView.as_view(),name='group delete'),
    path('edit_group/<int:pk>', views.EditGroup.as_view(), name='edit group'),
    path('logout/', views.logout_confirm, name='logout confirm'),
    path('profile/', include([
        path('<int:pk>', views.ProfileDetails.as_view(), name='profile'),
        path('edit/<int:pk>', views.ProfileEditView.as_view(), name='profile edit'),
        path('delete/<int:pk>', views.UserDeleteView.as_view(), name='profile delete')
    ])),
    path('add_student/', views.add_student, name='add student'),
    path('edit_student/<int:pk>', views.EditStudent.as_view(), name='edit student'),
path('delete_student/<int:pk>', views.DeleteStudentView.as_view(), name='delete student'),
path('create_group/', views.CreateGroup.as_view(), name='create group'),
]
