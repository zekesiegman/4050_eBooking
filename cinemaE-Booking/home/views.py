from django.shortcuts import render, redirect
from .models import User
from .models import Account
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.models import User as us

# Create your views here.

def registration2(response):
    form = UserCreationForm()
    return render(response, "../templates/registration2.html", {"form":form})

def registration(request):

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
        username = request.POST.get('username')
        tempName = request.POST.get('name')
        nameArr = tempName.split()
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = us.objects.create_user(username, email, password)
        user.first_name = nameArr[0]
        user.last_name = nameArr[1]
        user.is_staff = False
        user.is_active = False
        user.save()
        return render(request, '../templates/registration.html')
    else:
        return render(request, '../templates/registration.html')


def registration_success(request):
    return render(request, '../templates/registration_success.html')


def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, '../templates/logout.html')
    else:
        return render(request, '../templates/index.html')


def user_profile(request):
    users = User.objects.order_by('userId')
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
