from django.db.models import F

from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import Tickets
from ..serializers import (TicketsPurchaseListSerializer,
                           TicketsPurchaseSerializer)
from .base import BaseViewSet


class PurchaseTicketViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    BaseViewSet
):
    permission_classes = [AllowAny]

    serializer_action_classes = {
        "list": TicketsPurchaseListSerializer,
        "retrieve": TicketsPurchaseListSerializer,
        "purchase": TicketsPurchaseSerializer
    }

    queryset = Tickets.objects.annotate(available_count=F(
        'max_purchase_count') - F('purchased_count')).filter(available_count__gt=0)

    @action(methods=['POST'], detail=True)
    def purchase(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
