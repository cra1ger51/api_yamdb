from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import BasePermission


class CustomPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            if request.method == 'POST' and request.user.is_authenticated == True:
                return True
            elif obj.author == request.user or request.user.role in ('moderator','admin'):
                return True
        else:
            return True