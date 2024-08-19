from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Title, Category, Genre, Review
from .filters import TitleFilter
from .mixins import PutExclude, ListCreateDestroyViewSet
from .serializers import (
    SignupSerializer, TokenSerializer, UserSerializer, TitleSerializer,
    TitleGETSerializer, CategorySerializer, GenreSerializer,
    ReviewSerializer, CommentSerializer, MeSerializer
)
from .permissions import OwnerOrAdmin, ReadonlyOrAdmin, ReadonlyOrOwnerOrStaff
from .email_code import send_confirmation_code, generate_code


User = get_user_model()


class SignupAPIView(APIView):
    """APIView для регистрации пользователей."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = generate_code()
        user.confirmation_code = confirmation_code
        user.save()
        send_confirmation_code(
            email=user.email,
            confirmation_code=confirmation_code
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenAPIView(APIView):
    """APIView для получения токена."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        if confirmation_code == user.confirmation_code:
            token = str(AccessToken.for_user(user))
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response(
            {'confirmation_code': ['Код не действителен']},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (OwnerOrAdmin, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(PutExclude):
    """Вьюсет для создания объектов класса Title."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (ReadonlyOrAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleGETSerializer
        return TitleSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    """Вьюсет для создания объектов класса Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    """Вьюсет для создания объектов класса Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(PutExclude):
    """Вьюсет для создания отзывов к произведениям."""

    serializer_class = ReviewSerializer
    permission_classes = (ReadonlyOrOwnerOrStaff,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(title=self.get_title(), author=self.request.user)


class CommentViewSet(PutExclude):
    """Вьюсет для создания комментариев к отзывам."""

    serializer_class = CommentSerializer
    permission_classes = (ReadonlyOrOwnerOrStaff,)

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(), author=self.request.user)
