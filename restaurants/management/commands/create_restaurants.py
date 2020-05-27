from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from restaurants.models import Restaurants

owners = [
    {
        "first_name":"owner1",
        "email":"owner1@gmail.com",
        "password":"test",
        "username":"owner1"
    },
    {
        "first_name":"owner2",
        "email":"owner2@gmail.com",
        "password":"test",
        "username":"owner2"
    }
]

def load_user():
    for owner in owners:
        user = User.objects.create(first_name=owner["first_name"], email=owner["email"], username=owner["username"])
        user.set_password(owner["password"])
        user.save()

def load_restaurants():
    owner1 = User.objects.get(email="owner1@gmail.com", username="owner1")
    owner2 = User.objects.get(email="owner2@gmail.com", username="owner2")
    for i in range(1, 4):
        Restaurants.objects.create(name=("Restaurant{}").format(i), owner=owner1)
    for i in range(1, 4):
        Restaurants.objects.create(name=("Restaurant{}").format(i), owner=owner2)

class Command(BaseCommand):
    def handle(self, **options):
        load_user()
        load_restaurants()
