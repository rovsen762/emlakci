from django.shortcuts import render
from .models import Category,City, Area, Metro, Sight, Street, Location , Property, PropertySource, Notification
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

@login_required
def property_list(request):
    properties = Property.objects.all().order_by('-created_at')
    return render(request, 'property-list.html', {'properties': properties})



@login_required
def property_detail(request, pk):
    property = Property.objects.get(pk=pk)
    return render(request, 'property-detail.html', {'property': property})


@login_required
def property_grid(request):
    properties = Property.objects.all().order_by('-created_at')
    return render(request, 'property-grid.html', {'properties': properties})