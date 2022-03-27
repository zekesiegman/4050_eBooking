from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('index', views.index, name="index"),
    path('registration', views.registration, name="registration"),
    path('registration_success', views.registration_success, name="registration_success"),
    path('user-profile', views.user_profile, name="user-profile"),
    path('editprofile', views.editprofile, name="editprofile"),
    path('adminpage', views.adminpage, name="adminpage"),
    path('logoutpage', views.logoutpage, name="logoutpage"),
    path('registration2', views.registration2, name="registration2"),
    path('login', views.login, name="login"),

]
