import math
import threading

from django.db import connection
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from restaurants.models import Restaurants, Tickets
from .factories import OwnerFactory, RestaurantFactory, TicketFactory


def testing_concurrency(times):
    def test_concurrently_decorator(test_func):
        def wrapper(*args, **kwargs):
            exceptions = []
            def call_test_func():
                try:
                    test_func(*args, **kwargs)
                except Exception as e:
                    exceptions.append(e)
                    raise
            threads = []
            for i in range(times):
                threads.append(threading.Thread(target=call_test_func))
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            if exceptions:
                raise Exception('test_concurrently intercepted %s exceptions: %s' % (len(exceptions), exceptions))
        return wrapper
    return test_concurrently_decorator


class PurchaseTicketViewSetTests(APITestCase):
    def setUp(self):
        self.owner = OwnerFactory(
            email="test@gmail.com", first_name="test", password="test")
        for index1 in range(2):
            restaurant = RestaurantFactory(owner=self.owner)
            for index2 in range(5):
                ticket_name = f"Ticket_{index1}_{index2}"
                TicketFactory(
                    name=ticket_name, max_purchase_count=10, restaurant=restaurant)

    def test_list_purchase_tickets(self):
        """
        To all tickets of restaurant
        """
        list_endpoint = reverse('tickets-list')

        response = self.client.get(list_endpoint, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], Tickets.objects.count())

    def test_retrive_purchase_ticket(self):
        """
        To purchase tickets of restaurant
        """
        ticket = Tickets.objects.first()
        detail_endpoint = reverse('tickets-detail', args=(ticket.code,))

        response = self.client.get(detail_endpoint, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response_keys = (
            "name",
            "available_quantity",
            "code",
            "purchased_count",
            'restaurant',
            'detail_url',
        )
        for key in expected_response_keys:
            self.assertIn(key, response.json().keys())

    def test_purchase_ticket(self):
        ticket = Tickets.objects.first()
        data = {
            "email": "test@yopmail.com",
            "count": "10"
        }
        purchase_endpoint = reverse('tickets-purchase', args=(ticket.code, ))

        @testing_concurrency(10)
        def post_data():
            response = self.client.post(purchase_endpoint, data, format='json')
            print(response.json())
            connection.close()
        post_data()
