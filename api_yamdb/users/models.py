from django.db import models
from django.contrib.auth.models import AbstractUser

from .constants import MAX_LEGTH_USERNAME, USER, MODERATOR, ADMIN
from .validators import validate_username


class UserRole(models.TextChoices):
    USER = USER, 'Пользователь'
    MODERATOR = MODERATOR, 'Модератор'
    ADMIN = ADMIN, 'Администратор'


class User(AbstractUser):
    """Кастомная модель пользователя."""

    username = models.CharField(
        max_length=MAX_LEGTH_USERNAME,
        unique=True,
        validators=(validate_username,)
    )
    email = models.EmailField(unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        max_length=max(len(role) for role in UserRole),
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    confirmation_code = models.TextField('Код подтверждения', blank=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('date_joined',)

    @property
    def is_admin(self):
        return self.is_superuser or self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR
