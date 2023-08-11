from django.urls import include, path

from my_diary.account_app import views
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name='index.html'), name='index'),
    path('about/',views.about_view,name='about'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('logout/yes/', views.UserLogoutView.as_view(), name="logout"),

    path('logout/', views.logout_confirm, name='logout confirm'),
    path('profile/', include([
        path('<int:pk>', views.ProfileDetails.as_view(), name='profile'),
        path('edit/<int:pk>', views.ProfileEditView.as_view(), name='profile edit'),
        path('delete/<int:pk>', views.UserDeleteView.as_view(), name='profile delete')
    ])),
    path('create_subject/', views.CreateSubject.as_view(), name='create subject'),
    path('edit_subject/<int:pk>', views.EditSubject.as_view(), name='edit subject'),
    path('delete_subject/<int:pk>', views.DeleteSubject.as_view(), name='delete subject'),
]
