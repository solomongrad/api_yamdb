from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

CHOICES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    """Кастомная модель пользователя"""
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.TextField('Роль', default='user', choices=CHOICES)
    confirmation_code = models.TextField('Код подтверждения', blank=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def is_admin(self):
        return self.is_superuser or self.role == 'admin'

    def is_admin_or_moderator(self):
        return (self.is_superuser or self.role == 'admin'
                or self.role == 'moderator')
