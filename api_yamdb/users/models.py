from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class MyUser(AbstractUser):
    password = models.CharField(_('password'), max_length=128, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.TextField('Роль', default='user')
    confirmation_code = models.TextField('Код подтверждения', blank=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)
