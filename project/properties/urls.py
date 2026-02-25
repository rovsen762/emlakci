from .views import property_list,property_detail

from django.urls import path

urlpatterns = [
    path('list/', property_list, name='property-list'),
    path('detail/<int:pk>/', property_detail, name='property-detail'),
]