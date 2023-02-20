from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CommentViewSet,
                    ReviewViewSet,
                    TitleViewSet,
                    CategoryViewSet,
                    GenreViewSet)

v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
v1_router.register(
    r'titles', TitleViewSet
)
v1_router.register(
    r'categories', CategoryViewSet
)
v1_router.register(
    r'genres', GenreViewSet
)

urlpatterns = [
    path('', include('users.urls')),
    path('', include(v1_router.urls)),
]
