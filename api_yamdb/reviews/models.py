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


class Genre(models.Model):
    """Жанры."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Category(models.Model):
    """Категории."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Произведение."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения'
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска'
    )
    rating = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Рейтинг'
    )
    description = models.TextField()
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,  # тут просил поставить null-True, т.к. стоит SET_NULL
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['-id']

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Отношение произведения к жанру."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre}{self.title}'


class Review(models.Model):
    # SCORES = (
    #     (1, 2, 3, 4, 5, 6, 7, 8, 9, 10,),
    # )
    SCORES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6"),
        (7, "7"),
        (8, "8"),
        (9, "9"),
        (10, "10"),
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
        verbose_name='Оценка',
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
