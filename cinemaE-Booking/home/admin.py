from django.contrib import admin
from .models import Customer
from .models import User
from .models import UserStatus
from .models import UserType
from .models import Account
from .models import CardType
from .models import Promotion

# Register your models here.

admin.site.register(Customer)
admin.site.register(User)
admin.site.register(UserStatus)
admin.site.register(UserType)
admin.site.register(Account)
admin.site.register(CardType)
admin.site.register(Promotion)
