from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField, StringRelatedField
from rest_framework.serializers import (ModelSerializer,
                                        ValidationError)
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import (Category, Comment, Genre,
                            Review, Title, User)
from .validators import validate_username, validate_email


class CategorySerializer(ModelSerializer):
    # Добавил read_only=True, обязательный аргумент для рилейтед полей
    slug = SlugRelatedField(slug_field='title', read_only=True)

    def validate_slug(self, value):
        if Category.objects.filter(slug=value).exists():
            raise ValidationError(
                'Поле slug каждой категории должно быть уникальным!')
        return value

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(ModelSerializer):
    # Добавил read_only=True, обязательный аргумент для рилейтед полей
    slug = SlugRelatedField(slug_field='title', read_only=True)

    def validate_slug(self, value):
        if Category.objects.filter(slug=value).exists():
            raise ValidationError(
                'Поле slug каждого жанра должно быть уникальным!')
        return value

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Comment


class TitleSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    comments = CommentSerializer(
        many=True, required=False
    )
    # Добавил read_only=True, обязательный аргумент для рилейтед полей
    genre = StringRelatedField(read_only=True)
    # Добавил read_only=True, обязательный аргумент для рилейтед полей
    category = SlugRelatedField(slug_field='titles', read_only=True)

    class Meta:
        fields = '__all__'
        read_only_fields = ('id', 'rating', 'description',)
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author')
            )
        ]


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(allow_blank=False)
    username = serializers.CharField(max_length=150, allow_blank=False,
                                     validators=[validate_username])

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = default_token_generator.make_token(user)
        if str(confirmation_code) != data['confirmation_code']:
            raise ValidationError('Неверный код подтверждения')
        return data


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, allow_blank=False,
                                   validators=[validate_email])
    username = serializers.CharField(max_length=150, allow_blank=False,
                                     validators=[validate_username])

    class Meta:
        model = User
        fields = ('email', 'username')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['email', 'username']
            )
        ]

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150,
                                     validators=[validate_username],
                                     allow_blank=False)
    email = serializers.CharField(max_length=254, validators=[validate_email],
                                  allow_blank=False)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
