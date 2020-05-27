# -*- coding: utf-8 -*-

from rest_framework import serializers

from ..models import Restaurants, Tickets


class CurrentRestaurantDefault:
    def set_context(self, serializer_field):
        restaurant_id = serializer_field.context['view'].parent_pk
        self.restaurant = Restaurants.objects.get(id=restaurant_id)

    def __call__(self):
        return self.restaurant

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class TicketsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tickets
        fields = (
            "name",
            "available_quantity",
            "code",
            "purchase_url",
            "purchased_count"
        )


class TicketsCreateSerializer(serializers.ModelSerializer):
    restaurant = serializers.HiddenField(default=CurrentRestaurantDefault())

    class Meta:
        model = Tickets
        fields = (
            "name",
            "restaurant",
            "max_purchase_count"
        )


class TicketsUpdateSerializer(TicketsCreateSerializer):
    pass
