from django.shortcuts import render, redirect
from .models import User
from .models import Account
from .models import Movie
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.models import User as us
from .forms import RegisterForm
from .forms import AddMovie
from cryptography.fernet import Fernet
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from verify_email.email_handler import send_verification_email
from django.contrib import messages

# global variable for Fernet key
key = Fernet.generate_key()
fernet = Fernet(key)

# Create your views here.

#def success(request,uid):

  #  return render(request, "/")


def registration2(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            # inactiveUser = send_verification_email(response, form)
            # inactiveUser.save()
            form.save()
            name = form.cleaned_data['first_name']
            # send confirmation video
            template = render_to_string('../templates/email_template.html', {'name':name})
            email = EmailMessage(
                'Thanks for signing up for our movie site!',
                template,
                settings.EMAIL_HOST_USER,
                [form.cleaned_data['email']]
            )
            email.fail_silently = False
            email.send()
            return redirect('/')
            # return response(response, "../templates/registration2.html", {'form': form})
    form = RegisterForm()
    return render(response, "../templates/registration2.html", {"form": form})


def registration_success(request):
    return render(request, '../templates/registration_success.html')


def forgotpassword(request):
    username = request.POST.get('username')
    newpassword = request.POST.get('newpassword')
    # try to find user with matching email and change password
    try:
        user = us.objects.get(username=username)
        user.set_password(newpassword)
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

    # update user info
    if request.method == 'POST':
        user = request.user
        f = request.POST.get('fname')
        # if form element is filled out, update info
        if len(f) != 0:
            user.first_name = request.POST.get('fname')
        l = request.POST.get('lname')
        if len(l) != 0:
            user.last_name = request.POST.get('lname')
        p = request.POST.get('password')
        if len(p) != 0:
            user.set_password(request.POST.get('password'))
            update_session_auth_hash(request, us)
        enrollForPromotions = request.POST.get('promotion')
        if enrollForPromotions is not None:
            User.user.enrollForPromotions = True

        cardno = request.POST.get('cardno')
        exp = request.POST.get('exp')
        address = request.POST.get('address')
        # if card info is filled out, create new account and save it
        if len(cardno) != 0 and len(exp) != 0 and len(address) != 0:
            account = Account()

            # encrypt card number with Fernet
            global fernet
            cardNoEnc = fernet.encrypt(cardno.encode())
            account.cardNo = cardNoEnc

            account.expirationDate = exp
            account.billingAdd = address
            account.user_userID = user
            account.save()
        user.save()
        return redirect('/')
    return render(request, '../templates/editprofile.html', context)


def index(request):
    movies = Movie.objects.all()
    context = {'movies': movies}

    if request.method == 'POST':
        searchStr = request.POST.get('search')
        movieSearch = Movie.objects.filter(title=searchStr)
        context2 = {'movies': movieSearch}
        return render(request, '../templates.search.html', context2)

    return render(request, '../templates/index.html', context)


def adminpage(request):
    if request.method == "POST":
        form = AddMovie(request.POST)
        if form.is_valid():
            form.save()
            return render(request, '../templates/admin.html', {'form': form})
        else :
            messages.error(request, 'Please fill out all fields')
    else:
        form = AddMovie()
        return render(request, '../templates/admin.html', {'form': form})