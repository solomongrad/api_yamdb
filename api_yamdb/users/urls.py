from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (SignupAPIView, TokenAPIView, UserViewSet,
                    MeAPIView, UsernameViewSet)

app_name = 'users'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register(
    r'users/(?P<username>[\w.@+-]+)/',
    UsernameViewSet,
    basename='username'
)

urlpatterns = [
    path('auth/signup/', SignupAPIView.as_view()),
    path('auth/token/', TokenAPIView.as_view()),
    path('users/me/', MeAPIView.as_view()),
    path('', include(router.urls)),
]
