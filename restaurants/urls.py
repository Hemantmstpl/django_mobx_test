from django.conf.urls import include, url
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from . import views

router = routers.DefaultRouter()

router.register(r'restaurants', views.RestaurantsViewSet,
                basename='restaurants')

nested_router = nested_routers.NestedDefaultRouter(
    router, r'restaurants', lookup='restaurant')

nested_router.register(
    'tickets', views.TicketsModelViewSet, basename='tickets')

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'', include(nested_router.urls)),
]
