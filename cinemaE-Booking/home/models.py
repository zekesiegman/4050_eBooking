from django.db import models
from django.contrib.auth.models import User as us

# Create your models here.


class UserStatus(models.Model):
    userStatusID = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=45)


class UserType(models.Model):
    userTypeID = models.IntegerField(primary_key=True)
    userTypeName = models.CharField(max_length=45)


class Account(models.Model):
    accountID = models.IntegerField(primary_key=True)
    carNo = models.IntegerField()
    userID = models.IntegerField()
    type = models.CharField(max_length=45)
    expirationDate = models.DateField()
    billingAdd = models.CharField(max_length=45)
    # user_userID = models.ForeignKey('User', on_delete=models.CASCADE)


class User(models.Model):
    # userObj = models.OneToOneField(us, on_delete=models.CASCADE)
    userID = models.IntegerField(primary_key=True, default=1)
    firstName = models.CharField(max_length=45)
    lastName = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=45)
    phone = models.IntegerField()
    status = models.IntegerField()
    enrollForPromotions = models.CharField(max_length=45)
    userStatus = models.OneToOneField(UserStatus, on_delete=models.CASCADE)
    userType = models.OneToOneField(UserType, on_delete=models.CASCADE)


class CardType(models.Model):
    cardTypeID = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=45)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)