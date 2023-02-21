from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import User


class CustomPermission(BasePermission):
    """
    Проверяем и пропускаем дальше:
    1) На чтение - всех;
    2) На создание - авторизованных пользователей;
    3) На редактирование и удаление - авторов объектов, модераторов, админов.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or (request.method == 'POST' and request.user.is_authenticated)
            or (obj.author == request.user
                or request.user.is_authenticated
                and request.user.role in (User.MODERATOR, User.ADMIN))
        )


class IsAdminOrReadOnly(BasePermission):
    """
    Полный доступ к функционалу получает только админ.
    Остальные пользователи имеют тоступ только к методам
    'GET', 'HEAD' или 'OPTIONS'.
    """
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_staff
                         or request.user.role == User.ADMIN)))
