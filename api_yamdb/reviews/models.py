from datetime import datetime
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

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
                                 null=True, verbose_name='категория')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)


class GenreTitle(models.Model):
    """Модель для связывания жанров и произведений."""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre}'


class Review(models.Model):
    """Модель отзыва к произведению."""
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='автор')
    score = models.IntegerField(
        'Оценка',
        validators=[
            MinValueValidator(
                1,
                message='Введенная оценка ниже допустимой'
            ),
            MaxValueValidator(
                10,
                message='Введенная оценка выше допустимой'
            )
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение',
        null=True
    )

    class Meta:
        """Мета класс к отзыву."""
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title',),
                name='unique_author_title'
            ),
        )

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель Комментария."""
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='автор')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               verbose_name='Отзыв', related_name='comments')

    class Meta:
        """Мета класс Комментария"""
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
