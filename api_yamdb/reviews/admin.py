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

    def get_genre(self, object):
        """Получает жанр или список жанров произведения."""
        genre_list = object.genre.get_queryset()
        genre_str = ''
        for genre in genre_list:
            genre_str += ', ' + genre.name
        return genre_str.lstrip(', ')

    get_genre.short_description = 'Жанр/ы произведения'

    def count_reviews(self, object):
        """Вычисляет количество отзывов на произведение."""
        return object.reviews.count()

    count_reviews.short_description = 'Количество отзывов'

    def get_rating(self, object):
        """Вычисляет рейтинг произведения."""
        rating = object.reviews.aggregate(average_score=Avg('score'))
        if rating.get('average_score') == None:
            return None
        return round(rating.get('average_score'))

    get_rating.short_description = 'Рейтинг'

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
    list_filter = ('name',)
    search_fields = ('name', 'year', 'category')


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'genre',
        'title',
    )
    list_filter = ('genre',)
    search_fields = ('title',)


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


admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.empty_value_display = 'значение отсутствует'
