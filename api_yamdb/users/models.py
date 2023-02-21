from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER = 'user'
    ROLES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=ROLES,
        default=USER)

    class Meta:
        ordering = ('id',)
