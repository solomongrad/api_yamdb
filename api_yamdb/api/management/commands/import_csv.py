import csv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Импорт данных из CSV в базу данных'
    file_path = 'static/data/users.csv'

    def handle(self, *args, **options):
        try:
            with open(self.file_path, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    User.objects.create(
                        id=row.get('id'),
                        username=row['username'],
                        email=row['email'],
                        role=row.get('role'),
                        bio=row.get('bio'),
                        first_name=row.get('first_name'),
                        last_name=row.get('last_name')
                    )

            print(f'Успешно импортировано из {self.file_path}')
        except Exception as e:
            print(f'Ошибка импорта: {e}')
