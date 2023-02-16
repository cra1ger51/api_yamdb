from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import signup, token, UserViewset


v1_router = DefaultRouter()
v1_router.register(r'users', UserViewset, basename='users')

urlpatterns = [
    path('auth/token/', token),
    path('auth/signup/', signup),
    path('', include(v1_router.urls)),
]
