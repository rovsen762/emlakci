from .views import property_list, property_grid, property_detail

from django.urls import path

urlpatterns = [
    path('property-list/', property_list, name='property-list'),
    path('property-grid/', property_grid, name='property-grid'),
    path('property-detail/<int:pk>/', property_detail, name='property-detail'),
]