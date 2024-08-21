# Generated by Django 3.2 on 2024-08-21 15:35

import django.core.validators
from django.db import migrations, models
import reviews.modelfunc


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(reviews.modelfunc.current_year_definition, message='Значение года выпуска не может быть больше текущего года')], verbose_name='Год выпуска'),
        ),
    ]
