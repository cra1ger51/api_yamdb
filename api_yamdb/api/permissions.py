from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.user.role == 'admin':
            return True