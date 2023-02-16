from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrSuperuserPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        return False


class CustomPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            if request.method == 'POST' and request.user.is_authenticated == True:
                return True
            elif obj.author == request.user or request.user.role in ('moderator','admin'):
                return True
        else:
            return True
