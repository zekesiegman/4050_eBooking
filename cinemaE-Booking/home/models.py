from django.db import models
from django.contrib.auth.models import User as us
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class User(models.Model):
    user = models.OneToOneField(us, on_delete=models.CASCADE, default=1)
    userId = models.AutoField(primary_key=True)
    phone = models.IntegerField(default=20000000000)
    enrollForPromotions = models.BooleanField(null=True)

    def __str__(self):
        return self.user.username


class Account(models.Model):
    accountID = models.AutoField(primary_key=True)
    cardNo = models.IntegerField(default=1)
    expirationDate = models.DateField()
    billingAdd = models.CharField(max_length=45)
    type = models.ForeignKey('CardType', on_delete=models.CASCADE, default=1)
    user_userID = models.ForeignKey(us, on_delete=models.CASCADE, default=1)


class CardType(models.Model):
    cardTypeID = models.AutoField(primary_key=True)
    type = models.CharField(max_length=45)
