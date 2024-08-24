from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .abstract_models import ReviewCommentModel, CategoryGenreModel
from .constants import (MAX_SCORE_VALUE, MIN_SCORE_VALUE,
                        NAME_MAX_LENGTH, SYMBOLS_TO_SHOW)
from .validators import current_year_definition

User = get_user_model()


class Genre(CategoryGenreModel):
    """Модель жанров для произведений."""
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(CategoryGenreModel):
    """Модель категорий для произведений."""
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Название'
    )
    year = models.SmallIntegerField(
        'Год выпуска',
        validators=(
            MaxValueValidator(current_year_definition,
                              message=('Значение года выпуска не может быть '
                                       'больше текущего года')),
        )
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    genre = models.ManyToManyField(Genre, verbose_name='жанр')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, verbose_name='Категория')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:SYMBOLS_TO_SHOW]


class Review(ReviewCommentModel):
    """Модель отзыва к произведению."""

    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=(
            MinValueValidator(
                MIN_SCORE_VALUE,
                message='Введенная оценка ниже допустимой'
            ),
            MaxValueValidator(
                MAX_SCORE_VALUE,
                message='Введенная оценка выше допустимой'
            )
        )
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
