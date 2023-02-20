from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import signup, token, UserViewset


users_router = DefaultRouter()
users_router.register(r'users', UserViewset, basename='users')


urlpatterns = [
    path('auth/token/', token),
    path('auth/signup/', signup),
    path('', include(users_router.urls)),
]
