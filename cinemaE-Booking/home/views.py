from django.shortcuts import render, redirect
from .models import User
from .models import UserStatus
from .models import UserType
from .models import Account
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

# Create your views here.


def registration(request):
    users = User.objects.order_by('userID')
    usersStatus = UserStatus.objects.order_by('userStatusID')
    userTypes = UserType.objects.order_by('userTypeID')
    context = {'users': users, 'userStatus': usersStatus, 'userType': userTypes, }

    if request.GET.get('login_now') == "Login Now":
        if request.user.is_authenticated:
            return render(request, '../templates/index.html')
        if request.method == "GET":
            username = request.GET.get('loginEmail')
            password = request.GET.get('loginPass')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form = AuthenticationForm(request.GET)
                return render(request, '../templates/registration.html', {'form': form})
        else:
            form = AuthenticationForm()
            return render(request, '../templates/registration.html', {'form': form})

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


def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, '../templates/logout.html')
    else:
        return render(request, '../templates/index.html')


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


def adminpage(request):
    return render(request, '../templates/admin.html')
