from reviews.models import Title, Category, Genre
from rest_framework.relations import SlugRelatedField, StringRelatedField
from rest_framework.serializers import (CurrentUserDefault, ModelSerializer,
                                        ValidationError)
from rest_framework.validators import UniqueTogetherValidator


class CategorySerializer(ModelSerializer):
    slug = SlugRelatedField(slug_field='title')

    def validate_slug(self, value):
        if Category.objects.filter(slug=value).exists():
            raise ValidationError(
                'Поле slug каждой категории должно быть уникальным!')
        return value


    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(ModelSerializer):
    slug = SlugRelatedField(slug_field='title')

    def validate_slug(self, value):
        if Category.objects.filter(slug=value).exists():
            raise ValidationError(
                'Поле slug каждого жанра должно быть уникальным!')
        return value

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    comments = CommentSerializer(
        many=True, required=False
    )
    genre = StringRelatedField(

    category = models.ForeignKey(



    class Meta:
        fields = '__all__'
        read_only_fields = ('id', 'rating', 'description',)
        model = Title
