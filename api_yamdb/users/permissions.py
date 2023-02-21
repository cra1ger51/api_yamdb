from rest_framework.permissions import BasePermission

from .models import User


class IsAdminOrSuperuserPermission(BasePermission):
    """Проверка наличия прав доступа admin или superuser."""
    def has_permission(self, request, view):
        return (request.user.role == User.ADMIN or request.user.is_superuser
                or request.user.is_staff)
