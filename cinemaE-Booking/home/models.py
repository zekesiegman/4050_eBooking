from django.db import models

# Create your models here.


class User(models.Model):
    userID = models.IntegerField(primary_key=True, default=1)
    firstName = models.CharField(max_length=45)
    lastName = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=45)
    phone = models.IntegerField()
    status = models.IntegerField()
    enrollForPromotions = models.CharField(max_length=45)
    userType = models.IntegerField()


class UserStatus(models.Model):
    userStatusID = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=45)
    user_userID = models.ForeignKey('User', on_delete=models.CASCADE)


class UserType(models.Model):
    userTypeID = models.IntegerField(primary_key=True)
    userTypeName = models.CharField(max_length=45)
    user_userID = models.ForeignKey('User', on_delete=models.CASCADE)


class CardType(models.Model):
    cardTypeID = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=45)


class Account(models.Model):
    accountID = models.IntegerField(primary_key=True)
    carNo = models.IntegerField()
    userID = models.IntegerField()
    type = models.CharField(max_length=45)
    expirationDate = models.DateField()
    billingAdd = models.CharField(max_length=45)
    user_userID = models.ForeignKey('User', on_delete=models.CASCADE)
    cardtype_cardTypeID = models.ForeignKey('CardType', on_delete=models.CASCADE)


class Promotion(models.Model):
    promotionID = models.IntegerField(primary_key=True)
    promotionType = models.CharField(max_length=45)
    startDate = models.DateField()
    durationDay = models.IntegerField()
    # booking_bookingID = models.ForeignKey('Booking') add once Booking model is added
    # user_userID = models.ForeignKey('User', on_delete=models.CASCADE)
