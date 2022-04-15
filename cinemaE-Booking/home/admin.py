from django.contrib import admin
from .models import User
from .models import Account
from .models import CardType
from .models import Movie
from .models import Showtime
from .models import MovieCategory
from django.contrib.auth.admin import UserAdmin

class UserConfig(UserAdmin):
    search_fields = ('email','user_name','first_name',)
    ordering = ('email',)
    add_fieldsets = ((None, {'fields': ('username','date_joined',)}))
    list_display = ('email','user_name','first_name',
                    'last_name','is_active', 'is_staff')


# Register your models here.

admin.site.register(User, UserConfig)
admin.site.register(Account)
admin.site.register(CardType)
admin.site.register(Movie)
admin.site.register(Showtime)
admin.site.register(MovieCategory)
