from django.contrib import admin
from .models import User
from .models import Account
from .models import CardType
from .models import Movie
from .models import Showtime
from .models import MovieCategory
from django.contrib.auth.admin import UserAdmin

class UserConfig(UserAdmin):
    readonly_fields = ['date_joined','last_login']
    search_fields = ('email','username','first_name',)
    ordering = ('email',)
    #add_fieldsets = ((None, {'fields': ('username','date_joined',)}))
    list_display = ('email','username','first_name', 'password',
                    'last_name','is_active', 'is_superuser')


# Register your models here.

admin.site.register(User, UserConfig)
admin.site.register(Account)
admin.site.register(CardType)
admin.site.register(Movie)
admin.site.register(Showtime)
admin.site.register(MovieCategory)
