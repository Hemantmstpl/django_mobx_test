from django.db.models import QuerySet
from rest_framework import viewsets
from ..permissions import ValidParentPKPermission


class ActionSerializerMixin:
    def get_serializer_class(self):
        """
        look up serializers in `self.serializer_action_classes`
        a dict mapping of actions and corrospoding serializer classes
        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(ActionSerializerMixin, self).get_serializer_class()


class BaseViewSet(ActionSerializerMixin, viewsets.GenericViewSet):
    pass


class BaseModelViewSet(ActionSerializerMixin, viewsets.ModelViewSet):
    pass


class BaseNestedModelViewSet(BaseModelViewSet):
    """
        Base viewset class for nested models
    """

    parent_lookup = 'parent'
    parent_pk = None
    parent_queryset = None

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        return super().get_permissions() + [ValidParentPKPermission()]

    def get_parent_queryset(self):
        assert self.parent_queryset is not None, (
            "'%s' should either include a `parent_queryset` attribute, "
            "or override the `get_parent_queryset()` method."
            % self.__class__.__name__
        )

        parent_queryset = self.parent_queryset
        if isinstance(parent_queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            parent_queryset = parent_queryset.all()
        return parent_queryset

    def is_valid_parent_pk(self):
        parent_queryset = self.get_parent_queryset()
        if self.parent_pk is not None and parent_queryset.filter(id=self.parent_pk).exists():
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        # get parent_pk from url arguments
        self.parent_pk = kwargs.get('%s_pk' % self.parent_lookup)
        return super(BaseNestedModelViewSet, self).dispatch(request, *args, **kwargs)
