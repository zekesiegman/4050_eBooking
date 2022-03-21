from django.shortcuts import render
from .models import Customer
from .models import User
from .models import UserStatus
from .models import UserType
from .models import Account
from .models import CardType
from .models import Promotion

# Create your views here.


def home(request):
    customers = Customer.objects.order_by('last_name')
    users = User.objects.order_by('userID')
    usersStatus = UserStatus.objects.order_by('userStatusID')
    userTypes = UserType.objects.order_by('userTypeID')
    accounts = Account.objects.order_by('accountID')
    cardTypes = CardType.objects.order_by('cardTypeID')
    promotions = Promotion.objects.order_by('promotionID')
    context = {'customers': customers, 'users': users, 'userStatus': usersStatus, 'userType': userTypes,
               'accounts': accounts, 'cardType': cardTypes, 'promotions': promotions, }
    return render(request, '../templates/home.html', context)

