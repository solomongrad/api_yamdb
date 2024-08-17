from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters, permissions, status
from reviews.models import Title, Category, Genre, Review
from .filters import TitleFilter
from .mixins import (CreateListViewSet, RetrieveUpdateDeleteViewSet,
                     PutExclude, ListCreateDestroyViewSet)
from .serializers import (SignupSerializer, TokenSerializer,
                          UserSerializer, TitleSerializer,
                          TitleGETSerializer, CategorySerializer,
                          GenreSerializer, ReviewSerializer, CommentSerializer)
from .permissions import IsAdmin, ReadonlyOrAdmin, ReadonlyOrOwnerOrStaff
from .utils import send_confirmation_code

User = get_user_model()


class SignupAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        user = User.objects.filter(email=email).first()
        if user and username == user.username:
            send_confirmation_code(user, email)
            return Response({'email': email, 'username': username},
                            status=status.HTTP_200_OK)
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(
            user, data=request.data,
            partial=True,
            context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(CreateListViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class UsernameViewSet(RetrieveUpdateDeleteViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'


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
        user = self.request.user
        serializer.save(title=self.get_title(), author=user)


class CommentViewSet(PutExclude):
    """Вьюсет для создания комментариев к отзывам."""
    serializer_class = CommentSerializer
    permission_classes = (ReadonlyOrOwnerOrStaff,)

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(review=self.get_review(), author=user)
