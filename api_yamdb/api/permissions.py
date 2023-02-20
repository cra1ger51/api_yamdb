from rest_framework.permissions import BasePermission, SAFE_METHODS


class CustomPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method in SAFE_METHODS):
            return True
        elif (request.method == 'POST' and request.user.is_authenticated):
            return True
        elif (obj.author == request.user or request.user.is_authenticated
              and request.user.role in ('moderator', 'admin')):
            return True


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated
                    and (request.user.is_staff
                         or request.user.role == 'admin'))
