import django
from django.shortcuts import render
from accounts.models import Account, Plan, AccountCustomers, AccountFilters, AccountCustomerPreferries
# Create your views here.


def index(request):
    return render(request, 'index.html')