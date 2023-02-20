from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrSuperuserPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        return False


class CustomPermission(BasePermission):
    """
    Проверяем и пропускаем дальше:
    1) На чтение - всех;
    2) На создание - авторизованных пользователей;
    3) На редактирование и удаление - авторов объектов, модераторов, админов
    """
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or
                (request.method == 'POST' and request.user.is_authenticated) or
                (obj.author == request.user or
                 request.user.is_authenticated and
                 request.user.role in ('moderator', 'admin')))


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated
                    and (request.user.is_staff
                         or request.user.role == 'admin'))
