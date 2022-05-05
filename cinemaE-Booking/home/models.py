import datetime
from django.conf import settings
import django.utils.timezone
from django.db import models
from django.contrib.auth.models import User as us
from django.db.models.signals import post_save
from django.dispatch import receiver
from cryptography.fernet import Fernet

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(us, on_delete=models.CASCADE, default=1, primary_key=True)
    phone = models.IntegerField()
    enrollForPromotions = models.BooleanField(default=False)


class Account(models.Model):
    accountID = models.AutoField(primary_key=True)
    cardNo = models.CharField(max_length=250, default="", blank=True)
    exp = models.DateField(default=django.utils.timezone.now)
    billingAdd = models.CharField(max_length=45, default="", blank=True)
    user = models.ForeignKey(us, on_delete=models.CASCADE, default=1)


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


class Temp(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, default=1)


class Ticket(models.Model):
    ticketID = models.AutoField(primary_key=True)
    seatNum = models.IntegerField(default=1)
    price = models.IntegerField(default=10)
    showtimeID = models.ForeignKey('Showtime', on_delete=models.CASCADE, default='12/12/12 12:12')
    user = models.ForeignKey(us, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, blank=True, null=True)


class Showtime(models.Model):
    time = models.CharField(primary_key=True, max_length=50, default='12/12/12 12:12')
    movieID = models.ForeignKey('Movie', on_delete=models.CASCADE, default='')

    def createSeats(self):
        for i in range(1, 22):
            ticket = Ticket(seatNum=i, showtimeID=self)
            ticket.save()


class MovieCategory(models.Model):
    category = models.CharField(primary_key=True, max_length=50)


class Promotion(models.Model):
    promoID = models.AutoField(primary_key=True)
    amount = models.IntegerField(default=1)
    valid_thru = models.DateField(auto_now=False)


class CardEncr(models.Model):
    key = settings.ENCRYPT_KEY
    fernet = Fernet(key)


class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    total = models.IntegerField(default=0)
    numTickets = models.FloatField(default=0)
    userID = models.ForeignKey(us, on_delete=models.CASCADE, default=1)
    showtimeID = models.ForeignKey('Showtime', on_delete=models.CASCADE, default='12/12/12 12:12')
    accountID = models.ForeignKey('Account', on_delete=models.CASCADE, default=1, blank=True, null=True)


