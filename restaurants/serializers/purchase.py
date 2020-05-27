from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import APIException

from ..models import Purchase, Tickets


class PurchaseSerializer(serializers.ModelSerializer):
    ticket = serializers.CharField(read_only=True)

    class Meta:
        model = Purchase
        fields = '__all__'

    def check_ticket_availaility(self, ticket, count):
        if ticket.available_quantity == 0:
            raise APIException("No more tickets available")
        if not (ticket.available_quantity > 0 and ticket.available_quantity >= count):
            raise APIException(("Only {} ticket are available").format(ticket.available_quantity))
        return True

    @transaction.atomic
    def create(self, validated_data):
        try:
            ticket = Tickets.objects.get(code=self.context["ticket_code"])
            if self.check_ticket_availaility(ticket, validated_data["count"]):
                validated_data['ticket'] = ticket
                purchase = super(PurchaseSerializer, self).create(validated_data)
                ticket.purchased_count += validated_data["count"]
                ticket.save()
                return purchase
        except Tickets.DoesNotExist:
            raise APIException("Invalid ticket code")