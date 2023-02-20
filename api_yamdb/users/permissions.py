from rest_framework.permissions import BasePermission

from .models import ADMIN


class IsAdminOrSuperuserPermission(BasePermission):
    """Проверка наличия прав доступа admin или superuser."""
    def has_permission(self, request, view):
        return request.user.role == ADMIN or request.user.is_superuser
