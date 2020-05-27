from django.contrib import admin

from .models import Restaurants, Tickets

# Register your models here.


@admin.register(Restaurants)
class RestaurantsAdmin(admin.ModelAdmin):
    pass


@admin.register(Tickets)
class TicketsAdmin(admin.ModelAdmin):
    pass
