from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet, signup, token, UserViewset


v1_router = DefaultRouter()
v1_router.register(r'users', UserViewset, basename='users')
v1_router.register(
    r'title/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'title/(?P<title_id>\d+)/reviews/(?P<reviews_id>\d+)/comments',
    CommentViewSet,
    basename='comments'

urlpatterns = [
    path('auth/token/', token),
    path('auth/signup/', signup),
    path('', include(v1_router.urls)),
]
