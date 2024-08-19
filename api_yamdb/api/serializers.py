from django.contrib.auth import get_user_model
from django.db.models import Avg

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Title, Category, Genre, Review, Comment
from users.constants import MAX_LEGTH_USERNAME, MAX_LEGTH_EMAIL
from users.validators import validate_username

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для создания объекта класса User."""

    email = serializers.EmailField(max_length=MAX_LEGTH_EMAIL, required=True)
    username = serializers.CharField(
        max_length=MAX_LEGTH_USERNAME,
        required=True,
        validators=(validate_username,))

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if User.objects.filter(username=data.get('username'),
                               email=data.get('email')).exists():
            return data
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError({'username':
                  'Пользователь с указанным username уже существует.'})
        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError({'email':
                  'Пользователь с указанным email уже существует.'})
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор проверки кода подтверждения"""

    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=6, required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

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


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов пути /me"""

    role = serializers.CharField(read_only=True)

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


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleGETSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title при безопасных запросах."""
    rating = serializers.IntegerField(min_value=1, max_value=10,
                                      default=5, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title для всех запросов кроме безопасных."""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=True,
        allow_empty=False,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор Отзыва."""
    author = SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('author', 'title',)

    def validate(self, data):
        """Валидация отзыва."""
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(
                author_id=user.id, title_id=title_id
            ).exists():
                raise serializers.ValidationError('Вы уже оставили отзыв')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор Комментария."""
    author = SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('author', 'review',)
