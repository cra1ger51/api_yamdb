from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=ROLES,
        default='user')

    class Meta:
        ordering = ['-id']
