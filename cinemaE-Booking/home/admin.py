from django.contrib import admin
from .models import User
from .models import Account
from .models import CardType
from .models import Movie
from .models import Showtime
from .models import MovieCategory

# Register your models here.

admin.site.register(User)
admin.site.register(Account)
admin.site.register(CardType)
admin.site.register(Movie)
admin.site.register(Showtime)
admin.site.register(MovieCategory)
