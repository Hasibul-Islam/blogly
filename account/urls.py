from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('profile-create/', views.profile, name='profile-create'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.register, name='register'),
    path('registration-admin-blogly-2023/', views.register_admin, name='register_admin'),
    path('change-password/', views.change_password, name="change_password"),
    path('my-profile/', views.profile_view, name="profile_view"),
    path('update-password/', views.update_password, name='update_password'),
    path('password-changed-successfully/', views.password_changed_successfully, name='password_changed_successfully'),
]