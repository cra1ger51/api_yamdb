from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('title', 'review', 'author')


class TitleCreateSerializer(ModelSerializer):
    genre = serializers.SlugRelatedField(many=True, slug_field='slug',
                                         queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        fields = '__all__'
        model = Title


class TitleGetSerializer(ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer()

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', 'author')

    def validate(self, data):
        view = self.context.get('view')
        title = view.kwargs['title_id']
        if self.context['request'].method == 'POST':
            if Review.objects.filter(author=self.context['request'].user,
                                     title=title).exists():
                raise ValidationError(
                    'Только один обзор от одного пользователя!')
            return data
        return data
