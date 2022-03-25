from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    firstname = forms.CharField()
    lastname = forms.CharField()



    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "firstname", "lastname", "email", "password")
