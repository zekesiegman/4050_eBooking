from django.shortcuts import render
from .models import Customer

# Create your views here.


def home(request):
    customers = Customer.objects.order_by('last_name')
    context = {'customers': customers, }
    return render(request, '../templates/home.html', context)
