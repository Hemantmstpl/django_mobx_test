from rest_framework.permissions import BasePermission


class ValidParentPKPermission(BasePermission):
    """
    Allows access only owner belongs tickets/coupons.
    """

    def has_permission(self, request, view):
        return view.is_valid_parent_pk()
