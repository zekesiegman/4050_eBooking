from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('registration', views.registration, name="registration"),
    path('user-profile', views.user_profile, name="user-profile")
]
