from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .core import ReviewCommentModel
from .constants import MAX_SCORE_VALUE, MIN_SCORE_VALUE

User = get_user_model()


class Genre(models.Model):
    """Модель жанров для произведений."""
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='slug')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категорий для произведений."""
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='slug')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    year = models.IntegerField(
        'Год выпуска',
        validators=[
            MinValueValidator(0,
                              message=('Значение года выпуска не может '
                                       'быть отрицательным')),
            MaxValueValidator(int(datetime.now().year),
                              message=('Значение года выпуска не может быть '
                                       'больше текущего года'))
        ]
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle',
                                   verbose_name='жанр')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, verbose_name='Категория')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель для связывания жанров и произведений."""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Соотношение жанра с произведением'
        verbose_name_plural = 'Соотношение жанров с произведениями'
        ordering = ('id',)

    def __str__(self):
        return f'жанр/ы произведения "{self.title}": {self.genre}'


class Review(ReviewCommentModel):
    """Модель отзыва к произведению."""

    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(
                MIN_SCORE_VALUE,
                message='Введенная оценка ниже допустимой'
            ),
            MaxValueValidator(
                MAX_SCORE_VALUE,
                message='Введенная оценка выше допустимой'
            )
        ]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произведение'
    )

    class Meta(ReviewCommentModel.Meta):
        """Мета класс к отзыву."""

        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title',),
                name='unique_author_title'
            ),
        )


class Comment(ReviewCommentModel):
    """Модель Комментария."""

    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               verbose_name='Отзыв')

    class Meta(ReviewCommentModel.Meta):
        """Мета класс Комментария"""

        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
