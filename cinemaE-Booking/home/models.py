from django.db import models
from django.contrib.auth.models import User as us
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class User(models.Model):
    user = models.OneToOneField(us, on_delete=models.CASCADE, default=1)
    userId = models.AutoField(primary_key=True)
    phone = models.IntegerField(default=20000000000)
    enrollForPromotions = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Account(models.Model):
    accountID = models.AutoField(primary_key=True)
    cardNo = models.CharField(max_length=250)
    expirationDate = models.DateField()
    billingAdd = models.CharField(max_length=45)
    # type = models.ForeignKey('CardType', on_delete=models.CASCADE, default=1)
    user_userID = models.ForeignKey(us, on_delete=models.CASCADE, default=1)


class CardType(models.Model):
    cardTypeID = models.AutoField(primary_key=True)
    type = models.CharField(max_length=45)


class Movie(models.Model):
    title = models.CharField(primary_key=True, max_length=100)
    director = models.CharField(max_length=100)
    producer = models.CharField(max_length=100)
    synopsis = models.CharField(max_length=500)
    rating = models.CharField(max_length=5)
    playing_now = models.BooleanField(default=False)  # if movie is playing now or coming soon
    # reviews = ?
    # cast = ?
    trailer_picture = models.URLField(max_length=300, blank=True)
    trailer_video = models.URLField(max_length=250, blank=True)
    cat = models.ForeignKey('MovieCategory', on_delete=models.CASCADE, default='Action')


class Showtime(models.Model):
    time = models.CharField(primary_key=True, max_length=50, default='12/12/12 12:12')
    movieID = models.ForeignKey('Movie', on_delete=models.CASCADE, default='')


class MovieCategory(models.Model):
    category = models.CharField(primary_key=True, max_length=50)
