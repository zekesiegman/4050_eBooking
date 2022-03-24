from django.db import models
from django.contrib.auth.models import User as us

# Create your models here.


class User(models.Model):
    userId = models.IntegerField(primary_key=True, default=1)
    userObj = models.ForeignKey(us, on_delete=models.CASCADE, default=1)
    phone = models.IntegerField(default=20000000000)
    enrollForPromotions = models.BooleanField(null=True)

    def __str__(self):
        return self.enrollForPromotions

    def __str__(self):
        return self.phone


class Account(models.Model):
    accountID = models.AutoField(primary_key=True, default=1)
    carNo = models.IntegerField()
    expirationDate = models.DateField()
    billingAdd = models.CharField(max_length=45)
    type = models.ForeignKey('CardType', on_delete=models.CASCADE, default=1)
    user_userID = models.ForeignKey('User', on_delete=models.CASCADE, default=1)


class CardType(models.Model):
    cardTypeID = models.IntegerField(primary_key=True, default=1)
    type = models.CharField(max_length=45)
