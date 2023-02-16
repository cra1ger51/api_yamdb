from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, CategoryViewSet, GenreViewSet

routers = DefaultRouter()
routers.register(
    'titles', TitleViewSet
)
routers.register(
    'categories', CategoryViewSet
)
routers.register(
    'genre', GenreViewSet
)

urlpatterns = [
    path('', include(routers.urls)),
    #path('', include('djoser.urls')),
    #path('', include('djoser.urls.jwt')),
]
