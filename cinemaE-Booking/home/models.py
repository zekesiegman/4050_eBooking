from django.db import models

# Create your models here.


class Customer(models.Model): #test model
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class User(models.Model):
    userID = models.IntegerField()
    firstName = models.CharField(max_length=45)
    lastName = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=45)
    phone = models.IntegerField()
    status = models.IntegerField()
    enrollForPromotions = models.CharField(max_length=45)
    userType = models.IntegerField()


class UserStatus(models.Model):
    userStatusID = models.IntegerField()
    status = models.CharField(max_length=45)
    user_userID = models.IntegerField()


class UserType(models.Model):
    userTypeID = models.IntegerField()
    userTypeName = models.CharField(max_length=45)
    user_userID = models.IntegerField()


class Account(models.Model):
    accountID = models.IntegerField()
    carNO = models.IntegerField()
    userID = models.IntegerField()
    type = models.CharField(max_length=45)
    expirationDate = models.DateField()
    billingAdd = models.CharField(max_length=45)
    user_userID = models.IntegerField()
    cardtype_cardTypeID = models.IntegerField()


class CardType(models.Model):
    cardTypeID = models.IntegerField()
    type = models.CharField(max_length=45)


class Promotion(models.Model):
    promotionID = models.IntegerField()
    promotionType = models.CharField(max_length=45)
    startDate = models.DateField()
    durationDay = models.IntegerField()
    booking_bookingID = models.IntegerField()
    user_userID = models.IntegerField()
