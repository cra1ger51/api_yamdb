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
        max_length=9,
        choices=ROLES,
        default='user')

class Review(models.Model):
    SCORES = (
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    )
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(
        max_length=256,
        null=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        default=1,
    )
    score = models.IntegerField(
        choices=SCORES,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

class Comment(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        max_length=256, null=False, blank=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        default=1,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )