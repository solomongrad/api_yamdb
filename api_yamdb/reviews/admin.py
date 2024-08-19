from django.contrib import admin
from django.db.models import Avg

from .models import Title, Category, Genre, Comment, Review, GenreTitle


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
        'get_genre',
        'count_reviews',
        'get_rating'
    )
    list_display_links = ('pk', 'name',)
    list_filter = ('category', 'genre')
    search_fields = ('name', 'year', 'category')
    list_per_page = 20
    ordering = ('pk',)

    def get_queryset(self, request):
        return Title.objects.all().select_related(
            'category'
        ).prefetch_related('genre').annotate(rating=Avg('reviews__score'))

    @admin.display(description='Жанр/ы произведения')
    def get_genre(self, title):
        """Получает жанр или список жанров произведения."""
        genre_list = title.genre.get_queryset()
        genre_str = ''
        for genre in genre_list:
            genre_str += ', ' + genre.name
        return genre_str.lstrip(', ')

    @admin.display(description='Количество отзывов')
    def count_reviews(self, title):
        """Вычисляет количество отзывов на произведение."""
        return title.reviews.count()

    @admin.display(description='Рейтинг')
    def get_rating(self, title):
        """Вычисляет рейтинг произведения."""
        return round(title.rating)


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'genre',
        'title',
    )
    list_filter = ('genre',)
    search_fields = ('title',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'title',
                    'text',
                    'author',
                    'score',
                    'pub_date'
                    )
    search_fields = ('title__name', 'text')
    list_filter = ('title',)
    list_editable = ('text', 'author', 'score')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'text',
                    'review',
                    'author',
                    'pub_date'
                    )
    search_fields = ('text', 'review__text')
    list_filter = ('review',)
    list_editable = ('text', 'author')


admin.site.empty_value_display = 'значение отсутствует'
