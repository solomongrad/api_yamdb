from django.urls import include, path
from rest_framework.routers import DefaultRouter
<<<<<<< HEAD
from .views import (SignupAPIView, TokenAPIView, UserViewSet,
                    MeAPIView, UsernameViewSet, TitleViewSet,
                    CategoryViewSet, GenreViewSet)

app_name = 'api'

router_V1 = DefaultRouter()
router_V1.register('users', UserViewSet, basename='users')
=======

from .views import TitleViewSet, CategoryViewSet, GenreViewSet

router_V1 = DefaultRouter()
>>>>>>> 89077111e7bbcecb9157b698e59a6c6027fa57df
router_V1.register('titles', TitleViewSet)
router_V1.register('categories', CategoryViewSet, basename='categories')
router_V1.register('genres', GenreViewSet, basename='genres')

<<<<<<< HEAD
urlpatterns = [
    path('v1/auth/signup/', SignupAPIView.as_view()),
    path('v1/auth/token/', TokenAPIView.as_view()),
    path('v1/users/me/', MeAPIView.as_view()),
    path('v1/', include(router_V1.urls)),
    path('v1/users/<str:username>/', UsernameViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
=======

urlpatterns = [
    path('v1/', include(router_V1.urls)),
>>>>>>> 89077111e7bbcecb9157b698e59a6c6027fa57df
]
