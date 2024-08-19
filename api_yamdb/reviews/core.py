from django.db import models

from users.models import User


class ReviewCommentModel(models.Model):
    "Абмтрактный класс для Комментов и Отзывов"

    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='автор')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
