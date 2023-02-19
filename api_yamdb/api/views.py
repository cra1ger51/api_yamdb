from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Comment, Review, Title, User
from .permissions import (CustomPermission, IsAdminOrReadOnly,
                          IsAdminOrSuperuserPermission)
from .serializers import (CommentSerializer, ReviewSerializer,
                          SignUpSerializer, TitleGetSerializer,
                          TitleCreateSerializer, TokenSerializer,
                          UserSerializer, CategorySerializer, GenreSerializer)


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
    queryset = Review.objects.all()
    permission_classes = (CustomPermission, )

    def get_one_title(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title

    def update_title_rating(self):
        title = self.get_one_title()
        new_rating = (Review.objects.filter(
            title__exact=title.id).aggregate(Avg('score'))
        )
        title.update(rating=new_rating)

    def get_queryset(self):
        title = self.get_one_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_one_title()
        author = self.request.user
        serializer.save(author=author, title=title)
        self.update_title_rating()

    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        self.update_title_rating()

    def destroy(self, request, pk):
        review = Review.objects.get(pk=pk)
        review.delete()
        self.update_title_rating()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (CustomPermission, )

    def get_one_review(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Title, pk=review_id)
        return review

    def get_queryset(self):
        review = self.get_one_review()
        return review.comment.all()

    def perform_create(self, serializer):
        review = self.get_one_title()
        author = self.request.user
        serializer.save(author=author, review=review)


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsAdminOrSuperuserPermission)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def me(self, request):
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


def token_create(user):
    refresh = RefreshToken.for_user(user)
    token = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    response = {'token': str(token['access'])}
    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    Регистрация нового пользователя, отправка пода подтверждения.
    Формирование нового токена при повторной отправке запроса
    зарегистрированным пользователем.
    """
    serializer = SignUpSerializer(data=request.data)
    if User.objects.filter(username=request.data.get('username'),
                           email=request.data.get('email')).exists():
        user, created = User.objects.get_or_create(
            username=request.data.get('username')
        )
        if created is False:
            return token_create(user)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = User.objects.get(username=request.data['username'],
                            email=request.data['email'])
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    send_mail(f'Уважаемый, {str(user.username)}! Код подтверждения:',
              f' Ваш код подтверждени: {confirmation_code}',
              settings.EMAIL_SENDER,
              [request.data['email']],
              fail_silently=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    """
    Валидация кода подтверждения и формирование токена новому пользователю.
    """
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = get_object_or_404(User, username=request.data['username'])
        return token_create(user)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
