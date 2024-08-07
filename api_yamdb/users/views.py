from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters, mixins, permissions, status, viewsets
from .mixins import CreateListViewSet, RetrieveUpdateDeleteViewSet
from .serializers import SignupSerializer, TokenSerializer, MyUserSerializer
from .permissions import IsAdmin
from .utils import generate_code, send_confirmation_code

User = get_user_model()


class SignupAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        user = User.objects.filter(email=email).first()
        if user and username == user.username:
            confirmation_code = generate_code()
            send_confirmation_code(confirmation_code, email)
            user.confirmation_code = confirmation_code
            user.save()
            return Response(
                {'detail':
                 'Код подтверждения отправлен повторно.'},
                status=status.HTTP_200_OK)
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
        serializer = MyUserSerializer(user, context={'request': request})
        return Response(serializer.data)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = MyUserSerializer(
            user, data=request.data,
            partial=True,
            context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(CreateListViewSet):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class UsernameViewSet(RetrieveUpdateDeleteViewSet):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
