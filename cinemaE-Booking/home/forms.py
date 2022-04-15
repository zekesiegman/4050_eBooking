from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account
from .models import Movie
from .models import MovieCategory
from .models import Showtime
from django.forms import ModelForm
from django.contrib.auth import get_user_model


class RegisterForm(ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'style':'height: 50px;'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', 'style':'height: 50px;'}))
    phone = forms.CharField()
    enrollForPromotions = forms.BooleanField()
    class Meta(ModelForm):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2','phone','enrollForPromotions')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_name = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.password = self.cleaned_data['password1']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.enrollForPromotions = self.cleaned_data['enrollForPromotions']
        if commit:
            if self.cleaned_data['password1'] == self.cleaned_data['password2']:
                user.save()
        return user


class AddMovie(forms.Form):
    title = forms.CharField()
    director = forms.CharField()
    producer = forms.CharField()
    synopsis = forms.CharField()
    rating = forms.CharField()
    picture = forms.URLField()
    trailer = forms.URLField()
    category = forms.ModelChoiceField(queryset=MovieCategory.objects.all())

    class Meta():
        model = Movie
        fields = ('title', 'director', 'producer', 'synopsis', 'rating', 'picture',
                  'trailer', 'category')

    def save(self, commit=True):
        data = self.cleaned_data
        movie = Movie(title=data['title'], director=data['director'],
                    producer=data['producer'], synopsis=data['synopsis'],
                    rating=data['rating'], trailer_picture=data['picture'],
                    playing_now=True, trailer_video=data['trailer'], cat=data['category'])
        if commit:
            movie.save()
        return movie


class ScheduleMovie(forms.Form):
    time = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'MM/DD/YY HH:MM'}))
    movie = forms.ModelChoiceField(queryset=Movie.objects.all())

    class Meta():
        model = Showtime
        fields = ('time', 'movie')

    def save(self, commit=True):
        data = self.cleaned_data
        showtime = Showtime(time=data['time'], movieID=data['movie'])
        if commit:
            showtime.save()
        return showtime



