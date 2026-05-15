from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user.is_staff:
            return True

        if request.method in SAFE_METHODS:

            return request.user.id == obj.id

        return False
       