import pytz
import factory
from faker import Faker

from django.contrib.auth.models import User
from django.template import defaultfilters

from restaurants.models import Restaurants, Tickets, Purchase

faker = Faker()


class OwnerFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')

    class Meta:
        model = User


class RestaurantFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    owner = factory.SubFactory(OwnerFactory)

    class Meta:
        model = Restaurants


class TicketFactory(factory.django.DjangoModelFactory):
    code = factory.Faker('uuid4')
    name = factory.Faker('name')
    restaurant = factory.SubFactory(RestaurantFactory)

    class Meta:
        model = Tickets


class PurchaseFactory(factory.django.DjangoModelFactory):
    email = factory.Faker('email')
    ticket = factory.SubFactory(TicketFactory)

    class Meta:
        model = Purchase
