from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from reviews.models import Title, Category, Genre
from users.models import CHOICES
from .utils import send_confirmation_code

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать имя me в качестве username запрещено.')
        user = User.objects.create_user(email=email, username=username)
        send_confirmation_code(user, email)
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, read_only=True)
    confirmation_code = serializers.CharField(max_length=128, read_only=True)

    def validate(self, data):
        username = self.initial_data.get('username')
        confirmation_code = self.initial_data.get('confirmation_code')
        if username is None:
            raise serializers.ValidationError(
                'Необходимо указать username.')
        if confirmation_code is None:
            raise serializers.ValidationError(
                'Необходимо указать confirmation_code.')
        user = get_object_or_404(User, username=username)
        if (user.username == username
                and user.confirmation_code == confirmation_code):
            refresh = RefreshToken.for_user(user)
            return {'token': str(refresh.access_token)}
        raise serializers.ValidationError(
            'Неверное имя пользователя или код подтверждения.')


class MyUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=CHOICES, required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if not request.user.is_admin():
            validated_data.pop('role', None)
        if validated_data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя me в качестве username запрещено.')
        return super().update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleGETSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        if rating:
            return int(rating)
        return None


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')
