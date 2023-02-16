from rest_framework import permissions


class IsAdminOrSuperuserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        return False
