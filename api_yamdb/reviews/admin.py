from django.contrib import admin
from django.db.models import Avg

from .models import Title, Category, Genre, Comment, Review


class TitleAdmin(admin.ModelAdmin):

    def get_genre(self, object):
        """Получает жанр или список жанров произведения."""
        return '\n'.join((genre.name for genre in object.genre.all()))

    get_genre.short_description = 'Жанры произведения'

    def count_reviews(self, object):
        """Вычисляет количество отзывов на произведение."""
        return object.reviews.count()

    count_reviews.short_description = 'Количество отзывов'

    def get_rating(self, object):
        """Вычисляет рейтинг произведения."""
        rating = object.reviews.aggregate(average_score=Avg('score'))
        if rating:
            return round(rating.get('average_score'))
        return None

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
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    search_fields = ('name', 'year', 'category')


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
    empty_value_display = 'значение отсутствует'
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
    empty_value_display = 'значение отсутствует'
    list_editable = ('text', 'author')


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title, TitleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.empty_value_display = 'Не задано'
