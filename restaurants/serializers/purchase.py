from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.reverse import reverse

from ..models import Purchase, Tickets
from .tickets import TicketsListSerializer


class TicketsPurchaseSerializer(serializers.ModelSerializer):
    ticket = serializers.SerializerMethodField(method_name='get_ticket_name')

    class Meta:
        model = Purchase
        fields = '__all__'

    def check_ticket_availaility(self, ticket, count):
        if ticket.available_quantity == 0:
            raise APIException("No more tickets available")
        if not (ticket.available_quantity > 0 and ticket.available_quantity >= count):
            raise APIException(("Only {} ticket are available").format(
                ticket.available_quantity))
        return True

    @transaction.atomic
    def create(self, validated_data):
        ticket = self.context['view'].get_object()
        if self.check_ticket_availaility(ticket, validated_data["count"]):
            validated_data['ticket'] = ticket
            purchase = super().create(validated_data)
            ticket.purchased_count += validated_data["count"]
            ticket.save()
            return purchase

    def get_ticket_name(self, instance):
        return instance.ticket.name


class TicketsPurchaseListSerializer(TicketsListSerializer):
    restaurant = serializers.SerializerMethodField(
        method_name='get_restaurant_name')
    detail_url = serializers.SerializerMethodField(
        method_name='get_detail_url')

    class Meta(TicketsListSerializer.Meta):
        fields = TicketsListSerializer.Meta.fields + (
            'restaurant', 'detail_url')

    def get_restaurant_name(self, instance):
        return instance.restaurant.name

    def get_detail_url(self, instance):
        return reverse('tickets-detail', args=(instance.code, ))
