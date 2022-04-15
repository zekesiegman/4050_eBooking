from django.db import models
from django.contrib.auth.models import User as us, AbstractBaseUser,PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

# Create your models here.




class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username,password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active', True)
        return self.create_user(email, username, password, **other_fields)

    def create_user(self,email, username, password, **other_fields):
        if not email:
            raise ValueError('You must provide an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    cardNo = models.CharField(max_length=250,blank=True)
    expirationDate = models.DateField(default =datetime.date.today,blank=True)
    billingAdd = models.CharField(max_length=150,blank=True)
    phone = models.CharField(max_length=10)
    enrollForPromotions = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'username']


#class User(AbstractBaseUser):
 #   user = models.OneToOneField(us, on_delete=models.CASCADE, default=1)
  #  userId = models.AutoField(primary_key=True)
   # phone = models.IntegerField(default=20000000000)
    #enrollForPromotions = models.BooleanField(default=False)



class Account(models.Model):
    accountID = models.AutoField(primary_key=True)
    cardNo = models.CharField(max_length=250)
    expirationDate = models.DateField()
    billingAdd = models.CharField(max_length=45)
    # type = models.ForeignKey('CardType', on_delete=models.CASCADE, default=1)


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


class Promotion(models.Model):
    promoID = models.AutoField(primary_key=True)
    amount = models.IntegerField()
    valid_thru = models.DateField(auto_now=False)
