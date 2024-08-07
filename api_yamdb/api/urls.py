from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, CategoryViewSet, GenreViewSet

router_V1 = DefaultRouter()
router_V1.register('titles', TitleViewSet)
router_V1.register('categories', CategoryViewSet, basename='categories')
router_V1.register('genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('v1/', include(router_V1.urls)),
]
