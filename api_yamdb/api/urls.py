from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (SignupAPIView, TokenAPIView, UserViewSet,
                    MeAPIView, UsernameViewSet, TitleViewSet,
                    CategoryViewSet, GenreViewSet)

app_name = 'api'

router_V1 = DefaultRouter()
router_V1.register('users', UserViewSet, basename='users')
router_V1.register('titles', TitleViewSet)
router_V1.register('categories', CategoryViewSet, basename='categories')
router_V1.register('genres', GenreViewSet, basename='genres')

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
]
