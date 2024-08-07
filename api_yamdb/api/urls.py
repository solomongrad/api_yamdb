from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, TitleViewSet, ReviewViewSet

router_V1 = DefaultRouter()
router_V1.register('titles', TitleViewSet)
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


urlpatterns = [
    path('v1/', include(router_V1.urls)),
]
