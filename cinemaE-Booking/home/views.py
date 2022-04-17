from django.shortcuts import render, redirect
from .models import Account
from .models import Movie
from .models import Showtime
from .models import Profile
from .models import CardEncr
from .models import Promotion
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.models import User as us
from .forms import RegisterForm
from .forms import AddMovie
from .forms import ScheduleMovie
from .forms import CreatePromo
from .forms import SendPromo
from cryptography.fernet import Fernet
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from verify_email.email_handler import send_verification_email
from django.contrib import messages


# Create your views here.


def registration2(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # inactiveUser = send_verification_email(response, form)
            # inactiveUser.save()
            form.save()
            name = form.cleaned_data['first_name']
            # send confirmation email
            template = render_to_string('../templates/email_template.html', {'name':name})
            email = EmailMessage(
                'Thanks for signing up for our movie site!',
                template,
                settings.EMAIL_HOST_USER,
                [form.cleaned_data['email']]
            )
            email.fail_silently = True
            email.send()
            return redirect('/')
    form = RegisterForm()
    return render(request, "../templates/registration2.html", {"form": form})


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

    users = request.user
    accounts = Account.objects.get(user=users)
    profile = Profile.objects.get(user=users)
    context = {'users': users, 'accounts': accounts, 'profile': profile}
    return render(request, '../templates/user-profile.html', context)


def editprofile(request):
    accounts = Account.objects.get(user=request.user)
    context = {'accounts': accounts}

    # update user info
    if request.method == 'POST':
        user = request.user
        profile = Profile.objects.get(user=user)
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
        enroll = request.POST.get('promotion')
        if enroll == 'yes':
            profile.enrollForPromotions = True
        else:
            profile.enrollForPromotions = False
        t = request.POST.get('phone')
        if len(t) != 0:
            profile.phone = request.POST.get('phone')

        cardno = request.POST.get('cardno')
        exp = request.POST.get('exp')
        address = request.POST.get('address')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        state = request.POST.get('state')
        # if card info is filled out, create new account and save it
        if len(cardno) != 0 and len(exp) != 0 and len(address) != 0 and len(address1) != 0\
                and len(address2) != 0 and state is not None:

            # encrypt card number with Fernet
            fernet = CardEncr.fernet
            cardNoEnc = fernet.encrypt(cardno.encode())
            accounts.cardNo = cardNoEnc

            accounts.expirationDate = exp
            fullAddress = address + address1 + address2 + state
            accounts.billingAdd = fullAddress
        accounts.save()
        user.save()
        return redirect('/')
    return render(request, '../templates/editprofile.html', context)


def adminpage(request):
    if request.method == "POST":
        form = AddMovie(request.POST)
        form2 = ScheduleMovie()
        if form.is_valid():
            form.save()
            form = AddMovie()
            return render(request, '../templates/admin.html', {'form': form, 'form2': form2})
    else:
        form = AddMovie()
        form2 = ScheduleMovie()
        return render(request, '../templates/admin.html', {'form': form, 'form2': form2})
    if request.method == "POST" and not form.is_valid():
        form = AddMovie()
        form2 = ScheduleMovie(request.POST)
        if form2.is_valid():
            # check that show time doesn't exist already
            time = request.POST.get('time')
            count = Showtime.objects.filter(time=time).count()
            if count != 0:
                # error message
                return render(request, '../templates/admin.html', {'form': form, 'form2': form2})

            form2.save()
            # update movie info to now playing once movie is scheduled
            movietime = form2.cleaned_data['movie']
            movie = Movie.objects.filter(title=movietime)
            movie.playing_now = True

            form2 = ScheduleMovie()
            return render(request, '../templates/admin.html', {'form': form, 'form2': form2})
    else:
        form = AddMovie()
        form2 = ScheduleMovie()
        return render(request, '../templates/admin.html', {'form': form, 'form2': form2})


def index(request):
    movies = Movie.objects.all()
    context = {'movies': movies}

    if request.method == 'POST':
        searchStr = request.POST.get('search')
        movieSearch = Movie.objects.filter(title__icontains=searchStr)
        catSearch = Movie.objects.filter(cat=searchStr)
        matches = movieSearch | catSearch
        context2 = {'matches': matches}
        return render(request, '../templates/search.html', context2)

    return render(request, '../templates/index.html', context)


def search(request, new_context):
    context = new_context

    if request.method == 'POST':
        searchStr = request.POST.get('search')
        movieSearch = Movie.objects.filter(title__icontains=searchStr)
        catSearch = Movie.objects.filter(cat=searchStr)
        matches = movieSearch | catSearch
        context2 = {'matches': matches}
        return render(request, '../templates/search.html', context2)

    return render(request, '../templates/search.html', context)


def adminPromo(request):
    user = request.user
    profiles = Profile.objects.filter(enrollForPromotions=True)
    promos = Promotion.objects.all()
    form = CreatePromo()
    form2 = SendPromo()
    context = {'profile': profiles, 'promos': promos, 'form': form, 'form2': form2}
    if form.is_valid():
        form.save()

        # send promo to emails of users who enrolled for promotions
        if form2.is_valid():
            form2.send()

        newForm = CreatePromo()
        context = {'profile': profiles, 'promos': promos, 'form': newForm}
        return render(request, '../templates/admin-promo.html', context)
    return render(request, '../templates/admin-promo.html', context)
