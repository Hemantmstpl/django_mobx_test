from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from restaurants.models import Restaurants
from .factories import OwnerFactory, RestaurantFactory, TicketFactory, PurchaseFactory

class RestaurantTests(APITestCase):

    def setup(self):
        self.owner = OwnerFactory(email="test@gmail.com", first_name="test", password="test")

    def test_restaurant_list(self):
        """
        Ensure we can restaurants.
        """
        self.setup()
        RestaurantFactory(owner=self.owner, name="restaurant1")
        RestaurantFactory(owner=self.owner, name="restaurant2")
        RestaurantFactory(owner=self.owner, name="restaurant2")
        self.assertEqual(Restaurants.objects.count(), 3)
        endpoint = reverse('restaurants-choices')
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.owner)
        endpoint = reverse('restaurants-choices')
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)