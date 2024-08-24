from django.db import models

from .constants import NAME_MAX_LENGTH, SLUG_MAX_LENGTH, SYMBOLS_TO_SHOW
from users.models import User


class ReviewCommentModel(models.Model):
    "Абстрактный класс для Комментов и Отзывов."

    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='автор')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:SYMBOLS_TO_SHOW]


class CategoryGenreModel(models.Model):
    """Абстрактный класс для Жанров и Категорий."""
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=SLUG_MAX_LENGTH,
                            verbose_name='slug')

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:SYMBOLS_TO_SHOW]
