from ..serializers import PurchaseSerializer
from .base import BaseModelViewSet


class PurchaseViewSet(BaseModelViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = []
    authentication_classes = []
    http_method_names = ['post']

    def get_serializer_context(self):
    	context = super(PurchaseViewSet, self).get_serializer_context()
    	context["ticket_code"] = self.kwargs['ticket_code']
    	return context
