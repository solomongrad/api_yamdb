# Generated by Django 3.2 on 2024-08-21 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0012_alter_title_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(to='reviews.Genre', verbose_name='жанр'),
        ),
    ]