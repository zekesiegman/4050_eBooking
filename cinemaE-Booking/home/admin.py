from django.contrib import admin
from .models import Account
from .models import CardType
from .models import Movie
from .models import Showtime
from .models import MovieCategory
from .models import Profile
from .models import Promotion
from .models import Ticket
from .models import Order

# Register your models here.

admin.site.register(Account)
admin.site.register(CardType)
admin.site.register(Movie)
admin.site.register(Showtime)
admin.site.register(MovieCategory)
admin.site.register(Profile)
admin.site.register(Promotion)
admin.site.register(Ticket)
admin.site.register(Order)
