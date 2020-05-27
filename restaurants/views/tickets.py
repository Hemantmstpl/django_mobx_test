from ..models import Restaurants, Tickets
from ..serializers import (TicketsCreateSerializer, TicketsListSerializer,
                           TicketsUpdateSerializer)
from .base import BaseNestedModelViewSet

# Create your views here.


class BaseTicketsModelViewSet(BaseNestedModelViewSet):
    def get_parent_queryset(self):
        return Restaurants.objects.filter(owner=self.request.user)


class TicketsModelViewSet(BaseTicketsModelViewSet):

    parent_lookup = 'restaurant'

    serializer_action_classes = {
        "list": TicketsListSerializer,
        "create": TicketsCreateSerializer,
        "update": TicketsUpdateSerializer,
        "retrieve": TicketsListSerializer
    }

    def get_queryset(self):
        return Tickets.objects.filter(restaurant_id=self.parent_pk)
