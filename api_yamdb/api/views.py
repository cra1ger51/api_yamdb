from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from reviews.models import Category, Genre, Comment, Review, Title
from .permissions import CustomPermission, IsAdminOrReadOnly
from .serializers import (CommentSerializer,
                          ReviewSerializer,
                          TitleGetSerializer,
                          TitleCreateSerializer,
                          CategorySerializer,
                          GenreSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)

    @action(detail=False,
            methods=['delete'],
            url_path=r'(?P<slug>\w+)',
            lookup_field='slug')
    def destroy_category(self, request, slug):
        category = self.get_object()
        return Response(category.delete(), status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @action(detail=False,
            methods=['delete'],
            url_path=r'(?P<slug>\w+)',
            lookup_field='slug')
    def destroy_genre(self, request, slug):
        genre = self.get_object()
        return Response(genre.delete(), status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('year', 'name')
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Title.objects.all()
        genre = self.request.query_params.get('genre')
        category = self.request.query_params.get('category')
        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)
        elif category is not None:
            queryset = queryset.filter(category__slug=category)
        return queryset

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleCreateSerializer
        return TitleGetSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, CustomPermission)
    queryset = Review.objects.all()

    def get_one_title(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title

    def get_one_review(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review

    def update_title_rating(self):
        title = self.get_one_title()
        new_rating = (Review.objects.filter(
            title__exact=title.id).aggregate(Avg('score'))
        )
        title.rating = new_rating.get('score__avg')
        title.save()

    def one_author_one_review_check(self):
        title = self.get_one_title()
        if Review.objects.filter(title=title,
                                 author=self.request.user.id).exists():
            return False
        return True

    def get_queryset(self):
        title = self.get_one_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_one_title()
        author = self.request.user
        if self.one_author_one_review_check():
            serializer.save(author=author, title=title)
            self.update_title_rating()

    def perform_destroy(self, serializer):
        if self.request.user.role == 'user':
            if serializer.author != self.request.user:
                raise PermissionDenied('Вы не автор отзыва!')
            super().perform_destroy(serializer)
            self.update_title_rating()
        elif self.request.user.role in ('admin', 'moderator'):
            super().perform_destroy(serializer)
            self.update_title_rating()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, CustomPermission)

    def get_one_review(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review

    def get_one_title(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title

    def get_queryset(self):
        review = self.get_one_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_one_review()
        title = self.get_one_title()
        author = self.request.user
        serializer.save(author=author, review=review, title=title)
