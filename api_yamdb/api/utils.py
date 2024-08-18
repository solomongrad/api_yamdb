import random
import string
from django.core.mail import send_mail


def generate_code():
    all_symbols = string.ascii_uppercase + string.digits
    result = ''.join(random.choice(all_symbols) for _ in range(6))
    return result


def send_confirmation_code(user, email):
    confirmation_code = generate_code()
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email='notification@yamdb.com',
        recipient_list=[f'{email}'],
        fail_silently=True,
    )
    user.confirmation_code = confirmation_code
    user.save()
