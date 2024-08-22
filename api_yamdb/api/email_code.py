import random
import string

from django.conf import settings
from django.core.mail import send_mail

from users.constants import LEGTH_CONFIRMATION_CODE


def generate_code():
    """Генерация кода подтверждения."""

    all_symbols = string.ascii_uppercase + string.digits
    return ''.join(
        random.choice(all_symbols)
        for _ in range(LEGTH_CONFIRMATION_CODE)
    )


def send_confirmation_code(email, confirmation_code):
    """Oтправляет на почту пользователя код подтверждения."""

    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=(email,),
        fail_silently=False,
    )
