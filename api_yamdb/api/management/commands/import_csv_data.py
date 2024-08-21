import csv
import os

from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.conf import settings

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title
)

User = get_user_model()


class Command(BaseCommand):
    """Класс загрузки тестовой базы данных."""

    FILES_CLASSES = {
        'category': Category,
        'genre': Genre,
        'titles': Title,
        'genre_title': Title.genre.through,
        'users': User,
        'review': Review,
        'comments': Comment,
    }

    FIELDS = {
        'category': ('category', Category),
        'title_id': ('title', Title),
        'genre_id': ('genre', Genre),
        'author': ('author', User),
        'review_id': ('review', Review),
    }

    def open_csv_file(self, file_name):
        """Функция для открытия csv-файлов."""
        csv_file = file_name + '.csv'
        csv_path = os.path.join(settings.CSV_FILES_DIR, csv_file)
        try:
            with (open(csv_path, encoding='utf-8')) as file:
                return list(csv.reader(file))
        except FileNotFoundError:
            self.stdout.write(f'Файл {csv_file} не найден.')

    def change_foreign_values(self, data_csv):
        """Изменяет значения полей типа ForeignKey."""
        data_csv_copy = data_csv.copy()
        for field_key, field_value in data_csv.items():
            if field_key in self.FIELDS.keys():
                field_key0 = self.FIELDS[field_key][0]
                data_csv_copy[field_key0] = self.FIELDS[field_key][
                    1].objects.get(pk=field_value)
        return data_csv_copy

    def load_csv(self, file_name, class_name):
        """Загружает csv-файлы в таблицу."""
        columns, rows = self.open_csv_file(file_name)[0], self.open_csv_file(
            file_name)[1:]
        for row in rows:
            data_csv = dict(zip(columns, row))
            data_csv = self.change_foreign_values(data_csv)
            try:
                table = class_name(**data_csv)
                table.save()
            except (ValueError, IntegrityError) as error:
                self.stdout.write(
                    f'Ошибка в загружаемых данных. {error}. '
                    f'Таблица {class_name.__qualname__} не загружена.'
                )
                break
        self.stdout.write(f'Таблица {class_name.__qualname__} загружена.')

    def handle(self, *args, **options):
        for key, value in self.FILES_CLASSES.items():
            self.stdout.write(f'Загрузка таблицы {value.__qualname__}')
            self.load_csv(key, value)
