from django.contrib import admin

from .models import Restaurants, Tickets, Purchase

# Register your models here.
admin.site.register(Restaurants)
admin.site.register(Tickets)
admin.site.register(Purchase)