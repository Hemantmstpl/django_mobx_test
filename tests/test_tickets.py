from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from restaurants.models import Restaurants, Tickets
from .factories import OwnerFactory, RestaurantFactory, TicketFactory, PurchaseFactory


class TicketsTests(APITestCase):

    def setup(self):
        self.owner = OwnerFactory(email="test@gmail.com", first_name="test", password="test")
        self.restaurant = RestaurantFactory(owner=self.owner, name="restaurant1")

    def test_restaurant_list(self):
        """
        To get all tickets of restaurant
        """
        self.setup()
        self.assertEqual(Restaurants.objects.count(), 1)
        endpoint = reverse('tickets-list', kwargs={'restaurant_pk': self.restaurant.pk})

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.owner)
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        TicketFactory(name="ticket1", restaurant=self.restaurant)
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        restaurant2 = RestaurantFactory(owner=self.owner, name="restaurant2")
        TicketFactory(name="ticket1", restaurant=restaurant2)
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tickets.objects.count(), 2)
        self.assertEqual(response.data['count'], 1)

    def test_restaurant_create(self):
        """
        To create tickets of restaurant
        """
        self.setup()
        self.assertEqual(Restaurants.objects.count(), 1)
        data = {"name":"ticket1", "max_purchase_count":10}
        endpoint = reverse('tickets-list', kwargs={'restaurant_pk': self.restaurant.pk})

        response = self.client.post(endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Tickets.objects.count(), 0)

        self.client.force_authenticate(user=self.owner)
        response = self.client.post(endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tickets.objects.count(), 1)

    def test_ticket_retrieve(self):
        """
        To retrieve ticket of restaurant
        """
        self.setup()
        self.assertEqual(Restaurants.objects.count(), 1)
        ticket = TicketFactory(name="ticket1", restaurant=self.restaurant)
        endpoint = reverse('tickets-detail', kwargs={'restaurant_pk': self.restaurant.pk, 'pk':ticket.pk})

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.owner)
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "ticket1")

    def test_ticket_delete(self):
        """
        To delete a ticket of restaurant
        """
        self.setup()
        self.assertEqual(Restaurants.objects.count(), 1)
        ticket = TicketFactory(name="ticket1", restaurant=self.restaurant)
        endpoint = reverse('tickets-detail', kwargs={'restaurant_pk': self.restaurant.pk, 'pk':ticket.pk})

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(Tickets.objects.count(), 1)
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_ticket_update(self):
        """
        To update a ticket of restaurant
        """
        self.setup()
        self.assertEqual(Restaurants.objects.count(), 1)
        ticket = TicketFactory(name="ticket1", restaurant=self.restaurant, max_purchase_count=10)
        endpoint = reverse('tickets-detail', kwargs={'restaurant_pk': self.restaurant.pk, 'pk':ticket.pk})

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(ticket.max_purchase_count, 10)
        self.assertEqual(Tickets.objects.count(), 1)
        self.client.force_authenticate(user=self.owner)
        response = self.client.put(endpoint, data={"name":"ticket2", "max_purchase_count":5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "ticket2")
        self.assertEqual(response.data['max_purchase_count'], 5)
        self.assertEqual(Tickets.objects.get(pk=ticket.pk).max_purchase_count, 5)
