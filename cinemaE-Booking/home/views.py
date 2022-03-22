from django.shortcuts import render
from .models import User
from .models import UserStatus
from .models import UserType
from .models import Account
from .models import CardType

# Create your views here.


def home(request):
    users = User.objects.order_by('userID')
    usersStatus = UserStatus.objects.order_by('userStatusID')
    userTypes = UserType.objects.order_by('userTypeID')
    accounts = Account.objects.order_by('accountID')
    cardTypes = CardType.objects.order_by('cardTypeID')
    context = {'users': users, 'userStatus': usersStatus, 'userType': userTypes,
               'accounts': accounts, 'cardType': cardTypes, }
    return render(request, '../templates/home.html', context)


def registration(request):
    users = User.objects.order_by('userID')
    usersStatus = UserStatus.objects.order_by('userStatusID')
    userTypes = UserType.objects.order_by('userTypeID')
    context = {'users': users, 'userStatus': usersStatus, 'userType': userTypes, }
    return render(request, '../templates/registration.html', context)

def user_profile(request):
    return render(request, '../templates/user-profile.html')

def registration_success(request):
    return render(request, '../templates/registration_success.html')

def editprofile(request):
    return render(request, '../templates/editprofile.html')
def index(request):
    return render(request, '../templates/index.html')