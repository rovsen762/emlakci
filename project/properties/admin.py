from django.contrib import admin
from .models import Category, City, Area, Metro, Sight, Street, Location, Property, Notification, PropertySource
# Register your models here.
admin.site.register(Category)
admin.site.register(City)
admin.site.register(Area)
admin.site.register(Metro)
admin.site.register(Sight)
admin.site.register(Street)
admin.site.register(Location)
admin.site.register(Property)
admin.site.register(Notification)
admin.site.register(PropertySource)