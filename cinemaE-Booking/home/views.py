from django.shortcuts import render, redirect
from .models import User
from .models import Account
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.models import User as us
from .forms import RegisterForm
from django.conf import settings
from verify_email.email_handler import send_verification_email

# Create your views here.


def registration2(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            # inactiveUser = send_verification_email(response, form)
            form.save()
            return redirect('/')
            # return response(response, "../templates/registration2.html", {'form': form})
    form = RegisterForm()
    return render(response, "../templates/registration2.html", {"form": form,})


#def login(response):
 #   return render(response, "../templates/registration/login.html")

# old registration, no longer used but kept for reference
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

def forgotpassword(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
        user = us.objects.get(username=username)
        user.set_password(password)
        user.save()
        return redirect('/')
    except us.DoesNotExist:
        user = None
    return render(request, "../templates/forgotpassword.html")

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
    # users = User.objects.order_by('userID')
    accounts = Account.objects.order_by('accountID')
    context = {'accounts': accounts, }

    if request.method == 'POST':
        user = request.user
        f = request.POST.get('fname')
        if len(f) != 0:
            user.first_name = request.POST.get('fname')
        l = request.POST.get('lname')
        if len(l) != 0:
            user.last_name = request.POST.get('lname')
        p = request.POST.get('password')
        if len(p) != 0:
            user.set_password(request.POST.get('password'))
            update_session_auth_hash(request,us)
        cardno = request.POST.get('cardno')
        exp = request.POST.get('exp')
        address = request.POST.get('address')
        if cardno is not None and exp is not None and address is not None:
            account = Account()
            account.cardNo = cardno
            account.expirationDate = exp
            account.billingAdd = address
            account.type = 1
            account.user_userID = user
            account.save()
        user.save()
        #enrollForPromotions = request.POST.get('promotion')
        return redirect('/')
    return render(request, '../templates/editprofile.html', context)


def index(request):
    return render(request, '../templates/index.html')


def adminpage(request):
    return render(request, '../templates/admin.html')
