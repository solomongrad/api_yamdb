import random
import string
from django.core.mail import send_mail
from api_yamdb.settings import EMAIL_HOST_USER


def generate_code():
    """Генерирует код"""
    all_symbols = string.ascii_uppercase + string.digits
    return (''.join(random.choice(all_symbols) for _ in range(6)))


def send_confirmation_code(email, confirmation_code):
    """Oтправляет на почту пользователя код подтверждения."""
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=EMAIL_HOST_USER,
        recipient_list=(email,),
        fail_silently=False,
    )
