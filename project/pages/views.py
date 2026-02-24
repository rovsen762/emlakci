import django
from django.shortcuts import redirect, render
from accounts.models import Account, Plan, AccountCustomers, AccountFilters, AccountCustomerPreferries
from functools import wraps
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')  
def index(request):
    return render(request, 'index.html')