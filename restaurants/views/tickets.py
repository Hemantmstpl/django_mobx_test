from ..models import Restaurants, Tickets
from ..serializers import TicketsCreateSerializer, TicketsListSerializer
from .base import BaseNestedModelViewSet

# Create your views here.


class BaseTicketsModelViewSet(BaseNestedModelViewSet):
    def get_parent_queryset(self):
        return Restaurants.objects.filter(owner=self.request.user)


class RestaurantTicketsModelViewSet(BaseTicketsModelViewSet):

    parent_lookup = 'restaurant'

    serializer_action_classes = {
        "list": TicketsListSerializer,
        "create": TicketsCreateSerializer,
        "update": TicketsCreateSerializer,
        "retrieve": TicketsListSerializer
    }

    def get_queryset(self):
        return Tickets.objects.filter(restaurant_id=self.parent_pk)
