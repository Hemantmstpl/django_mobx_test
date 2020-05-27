from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Restaurants
from ..serializers import RestaurantsSerializer
from .base import BaseViewSet

# Create your views here.


class RestaurantsViewSet(BaseViewSet):

    serializer_class = RestaurantsSerializer

    def get_queryset(self):
        return Restaurants.objects.filter(owner=self.request.user)

    @action(methods=['GET'], detail=False)
    def choices(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
