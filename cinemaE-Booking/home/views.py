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
    if request.method == 'POST':
        user = User()
        tempName = request.POST.get('name')
        nameArr = tempName.split()
        user.firstName = nameArr[0]
        user.lastName = nameArr[1]
        user.email = request.POST.get('email')
        user.password = request.POST.get('password')
        user.save()
        return render(request, '../templates/registration.html', context)
    else:
        return render(request, '../templates/registration.html', context)


def registration_success(request):
    return render(request, '../templates/registration_success.html')


def user_profile(request):
    users = User.objects.order_by('userID')
    accounts = Account.objects.order_by('accountID')
    context = {'users': users, 'accounts': accounts, }
    return render(request, '../templates/user-profile.html', context)


def editprofile(request):
    users = User.objects.order_by('userID')
    accounts = Account.objects.order_by('accountID')
    context = {'users': users, 'accounts': accounts, }
    return render(request, '../templates/editprofile.html', context)


def index(request):
    return render(request, '../templates/index.html')
