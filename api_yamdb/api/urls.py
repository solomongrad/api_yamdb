from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    SignupAPIView, TokenAPIView, UserViewSet,
    TitleViewSet, CategoryViewSet, GenreViewSet,
    ReviewViewSet, CommentViewSet
)

app_name = 'api'

router_V1 = DefaultRouter()
router_V1.register('users', UserViewSet)
router_V1.register('titles', TitleViewSet)
router_V1.register('categories', CategoryViewSet, basename='categories')
router_V1.register('genres', GenreViewSet, basename='genres')
router_V1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_V1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_urls = [
    path('signup/', SignupAPIView.as_view()),
    path('token/', TokenAPIView.as_view()),
]

v1_urlpatterns = [
    path('auth/', include(auth_urls)),
    path('', include(router_V1.urls)),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
]
