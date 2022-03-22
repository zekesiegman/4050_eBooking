from django.contrib import admin
from .models import User
from .models import UserStatus
from .models import UserType
from .models import Account
from .models import CardType

# Register your models here.

admin.site.register(User)
admin.site.register(UserStatus)
admin.site.register(UserType)
admin.site.register(Account)
admin.site.register(CardType)
