from django.shortcuts import render, redirect, HttpResponse
from .models import Account
from .models import Movie
from .models import Showtime
from .models import Profile
from .models import CardEncr
from .models import Promotion
from .models import Ticket
from .models import Order
from .models import MovieCategory
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
from django import template
import json
from .models import Temp
from verify_email.email_handler import send_verification_email
from django.contrib import messages
from django.template import RequestContext
from django.urls import reverse
from datetime import datetime


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
    if request.method == 'POST':
        username = request.POST.get('username')
        newpassword = request.POST.get('newpassword')
        # try to find user with matching email and change password
        try:
            user = us.objects.get(username=username)
            user.set_password(newpassword)
            user.save()
            return redirect('/')
        except us.DoesNotExist:
            error = True
            return render(request, "../templates/forgotpassword.html", {'error': error})
    return render(request, "../templates/forgotpassword.html")


def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, '../templates/logout.html')
    else:
        return render(request, '../templates/index.html')


def user_profile(request):
    users = request.user
    cards = Account.objects.filter(user=users)
    firs = Account.objects.filter(user=users).first()
    cardList = []
    if cards.count() == 0 or len(firs.billingAdd) == 0:
        accountRemaining = 3
    else:
        accountRemaining = 3 - cards.count()
        for card in cards:
            cardno = card.cardNo
            fernet = CardEncr.fernet
            bites = bytes(cardno, 'utf-8')
            decoded = fernet.decrypt(bites).decode()
            decoded = decoded[-4:]
            cardList.append(decoded)
    profile = Profile.objects.get(user=users)
    orders = Order.objects.filter(userID=users)
    context = {'users': users, 'accountRemain': accountRemaining, 'profile': profile,
               'orders': orders, 'cards': cardList}
    return render(request, '../templates/user-profile.html', context)


def editprofile(request):
    context = {}
    # update user info
    if request.method == 'POST':
        users = request.user
        profile = Profile.objects.get(user=users)
        orders = Order.objects.filter(userID=users)
        cards = Account.objects.filter(user=users)
        context = {'users': users, 'profile': profile,
                   'orders': orders,'cards': cards}
        f = request.POST.get('fname')
        # if form element is filled out, update info
        if len(f) != 0:
            users.first_name = request.POST.get('fname')
        l = request.POST.get('lname')
        if len(l) != 0:
            users.last_name = request.POST.get('lname')
        p = request.POST.get('password')
        if len(p) != 0:
            users.set_password(request.POST.get('password'))
            update_session_auth_hash(request, us)
        enroll = request.POST.get('promotion')
        if enroll == 'yes':
            profile.enrollForPromotions = True
        else:
            profile.enrollForPromotions = False
        t = request.POST.get('phone')
        if len(t) != 0:
            profile.phone = request.POST.get('phone')
        users.save()
        return HttpResponse(user_profile(request))
    return render(request, '../templates/editprofile.html', context)


def addCard(request):
    user = request.user
    count = Account.objects.filter(user=user).count()
    profile = Profile.objects.get(user=user)
    temp = Account.objects.filter(user=user).first()
    context = {}
    if request.method == "POST" and count < 3:
        if count == 1 and len(temp.billingAdd) == 0:
            accounts = Account.objects.get(user=user)
        else:
            accounts = Account(user=user)
        cardno = request.POST.get('cardno')
        exp = request.POST.get('exp')
        address = request.POST.get('address')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        state = request.POST.get('state')
        s = str(state)
        # if card info is filled out, create new account and save it
        if len(cardno) != 0 or len(exp) != 0 or len(address) != 0 or len(address1) != 0 \
            or len(address2) != 0 or s is not None:
            # encrypt card number with Fernet
            fernet = CardEncr.fernet
            cardno = cardno.encode()
            cardNoEnc = fernet.encrypt(cardno).decode()
            accounts.cardNo = cardNoEnc
            accounts.exp = exp
            fullAddress = address + address1 + address2 + s
            accounts.billingAdd = fullAddress
            accounts.save()
            users = request.user
            return HttpResponse(user_profile(request))
    return render(request, '../templates/add-card.html', context)


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
                error = True
                return render(request, '../templates/admin.html', {'form': form, 'form2': form2, 'error': error})

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
    playing_now = Movie.objects.filter(playing_now=True)[:5]
    coming_soon = Movie.objects.filter(playing_now=False)[:5]
    context = {'playing_now': playing_now, 'coming_soon': coming_soon}

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
        context2 = {'matches': matches, }
        return render(request, '../templates/search.html', context2)

    return render(request, '../templates/search.html', context)


def adminPromo(request):
    promos = Promotion.objects.all()
    if request.method =="POST":
        form = CreatePromo(request.POST)
        form2 = SendPromo()
        if form.is_valid():
            form.save()
            form = CreatePromo()
            return render(request, '../templates/admin-promo.html', {'promos': promos, 'form': form, 'form2': form2})
        # send promo to emails of users who enrolled for promotions
    if request.method == "POST" and not form.is_valid():
        form = CreatePromo()
        form2 = SendPromo(request.POST)
        if form2.is_valid():
            users = us.objects.filter(is_staff=False)
            promo = form2.cleaned_data['promos']
            for user in users:
                profile = Profile.objects.get(user=user)
                print(profile.enrollForPromotions)
                if profile.enrollForPromotions:
                    emailAddr = user.email
                    name = user.first_name
                    promoId = promo.promoID
                    promoAmount = promo.amount
                    promoValid = promo.valid_thru
                    template = render_to_string('../templates/email-template2.html',
                                                {'name': name, 'id': promoId, 'amount': promoAmount, 'valid': promoValid})
                    email = EmailMessage(
                        'We have a new promotion for you!',
                        template,
                        settings.EMAIL_HOST_USER,
                        [emailAddr]
                    )
                    email.fail_silently = True
                    email.send()
            form2 = SendPromo()
            return render(request, '../templates/admin-promo.html', {'promos': promos, 'form': form, 'form2': form2})

    form = CreatePromo()
    form2 = SendPromo()
    return render(request, '../templates/admin-promo.html', {'promos': promos, 'form': form, 'form2': form2})


def booking(request):
    moviestring = ''
    if request.method == 'GET':
        moviestring = request.GET.get('movie')
    movie = Movie.objects.get(title=moviestring)
    showtimes = Showtime.objects.filter(movieID=movie)
    context = {'movie': movie, 'showtimes': showtimes}
    return render(request, '../templates/movieselect.html', context)


def seatselect(request):
    user = request.user
    num = chr(65)
    showtimeString = request.GET.get('time')
    showtime = Showtime.objects.get(time=showtimeString)
    movie = showtime.movieID
    seats = Ticket.objects.filter(showtimeID=showtime)
    context = {'movie': movie, 'showtime': showtime, 'seats': seats, 'num': num, 'user': user}
    if request.method == 'POST':
        selectedSeats = request.POST.getlist('seat')
        if len(selectedSeats) == 0:
            error = True
            context = {'movie': movie, 'showtime': showtime, 'seats': seats, 'num': num, 'user': user, 'error': error}
            return render(request, '../templates/seatselection.html', context)
        for seat in selectedSeats:
            ticket = Ticket.objects.get(seatNum=seat, showtimeID=showtime)
            ticket.user = request.user
            ticket.save()
        return redirect(reverse('orderedit') + '?time=' + showtimeString)
    return render(request, '../templates/seatselection.html', context)


def orderedit(request):
    user = request.user
    time = request.GET.get('time')
    showtime = Showtime.objects.get(time=time)
    showtimeString = showtime.time
    movie = showtime.movieID
    ticketCount = Ticket.objects.filter(user=user, showtimeID=showtime).count()
    context = {'showtime': showtime, 'movie': movie}
    if request.method == 'POST':
        adult = int(request.POST.get('adult'))
        child = int(request.POST.get('child'))
        senior = int(request.POST.get('senior'))
        totalCount = adult + child + senior
        changeCount = child + senior
        if totalCount != ticketCount:
            error = True
            context = {'showtime': showtime, 'movie': movie, 'error': error}
            return render(request, '../templates/order_edit.html', context)
        else:
            tickets = Ticket.objects.filter(user=user, showtimeID=showtime)[:changeCount]
            for ticket in tickets:
                ticket.price = 5
                ticket.save()
        return redirect(reverse('checkout') + '?time=' + showtimeString)
    return render(request, '../templates/order_edit.html', context)


def checkout(request):
    context = {}
    user = request.user
    time = request.GET.get('time')
    showtime = Showtime.objects.get(time=time)
    movie = showtime.movieID
    accounts = Account.objects.filter(user=user)
    numAccounts = accounts.count()
    tickets = Ticket.objects.filter(user=user, showtimeID=showtime)
    ticketCount = tickets.count()
    seatPrices = 0
    for ticket in tickets:
        seatPrices += ticket.price
    tax = round((seatPrices * .07), 3)
    total = seatPrices + tax
    cardApplied = False
    context = {'showtime': showtime, 'movie': movie, 'tickets': tickets, 'seatprices': seatPrices,
               'tax': tax, 'total': total, 'accounts': accounts, 'cardApplied': cardApplied}
    if request.method == 'POST':
        formName = request.POST.get('name')
        if formName == 'cardsForm':
            card = request.POST.get('card')
            account = Account.objects.get(accountID=card)
            order = Order(total=total, numTickets=ticketCount, userID=user, showtimeID=showtime, accountID=account)
            order.save()
            for ticket in tickets:
                ticket.order = order
                ticket.save()
            cardApplied = True
            context = {'showtime': showtime, 'movie': movie, 'tickets': tickets, 'seatprices': seatPrices,
                       'tax': tax, 'total': total, 'accounts': accounts, 'cardApplied': cardApplied}
            return render(request, '../templates/checkout.html', context)
        if formName == 'cardinfoForm' and numAccounts < 3:
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zip = request.POST.get('zip')
            ccnum = request.POST.get('cardnumber')
            exp = request.POST.get('exp')
            if len(address) != 0 and len(city) != 0 and len(zip) != 0 and len(ccnum) != 0 and len(exp) != 0 or state is not None:
                billingAdd = address + city + str(state) + zip
                fernet = CardEncr.fernet
                cardno = ccnum.encode('utf-8')
                cardNoEnc = fernet.encrypt(cardno).decode()
                account = Account(cardNo=cardNoEnc, exp=exp, billingAdd=billingAdd, user=user)
                account.save()
                order = Order(total=total, numTickets=ticketCount, userID=user, showtimeID=showtime, accountID=account)
                order.save()
                for ticket in tickets:
                    ticket.order = order
                    ticket.save()
                cardApplied = True
                context = {'showtime': showtime, 'movie': movie, 'tickets': tickets, 'seatprices': seatPrices,
                           'tax': tax, 'total': total, 'accounts': accounts, 'cardApplied': cardApplied}
                return render(request, '../templates/checkout.html', context)
            else:
                errorNewCard = True
                context = {'showtime': showtime, 'movie': movie, 'tickets': tickets, 'seatprices': seatPrices,
                    'tax': tax, 'total': total, 'accounts': accounts, 'errorNewCard': errorNewCard}
                return render(request, '../templates/checkout.html', context)
        if formName == 'promoForm':
            promoID = request.POST.get('promo')
            try:
                promo = Promotion.objects.get(promoID=promoID)
            except Promotion.DoesNotExist:
                errorPromo = True
                context = {'showtime': showtime, 'movie': movie, 'tickets': tickets, 'seatprices': seatPrices,
                           'tax': tax, 'total': total, 'accounts': accounts, 'errorPromo': errorPromo}
                return render(request, '../templates/checkout.html', context)
            total = round((total - promo.amount), 2)
            order = Order.objects.get(showtimeID=showtime, userID=user)
            order.total = total
            order.save()
            context = {'showtime': showtime, 'movie': movie, 'tickets': tickets, 'seatprices': seatPrices,
                       'tax': tax, 'total': total, 'accounts': accounts}
            return render(request, '../templates/checkout.html', context)
    return render(request, '../templates/checkout.html', context)


def orderconfirm(request):
    user = request.user
    time = request.GET.get('time')
    showtime = Showtime.objects.get(time=time)
    movie = showtime.movieID
    tickets = Ticket.objects.filter(user=user, showtimeID=showtime)
    order = Order.objects.get(userID=user, showtimeID=showtime)
    name = user.first_name
    emailAddr = user.email
    template = render_to_string('../templates/email_template3.html',
                                {'name': name, 'showtime': showtime, 'movie': movie, 'tickets': tickets, 'order': order})
    email = EmailMessage(
        'Your order has been set',
        template,
        settings.EMAIL_HOST_USER,
        [emailAddr]
    )
    email.fail_silently = True
    email.send()
    context = {'showtime': showtime, 'movie': movie, 'tickets': tickets, 'order': order}
    return render(request, '../templates/confirmation.html', context)


