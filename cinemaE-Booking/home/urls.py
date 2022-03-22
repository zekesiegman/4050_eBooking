from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('registration', views.registration, name="registration"),
    path('user-profile', views.user_profile, name="user-profile"),
    path('registration_success',views.registration_success,name ="registration_success"),
    path('editprofile',views.editprofile,name="editprofile"),
    path('index',views.index,name="index")
]
