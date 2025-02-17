# Generated by Django 5.1.3 on 2024-11-07 10:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "genre_name",
                    models.CharField(max_length=100, verbose_name="название жанра"),
                ),
            ],
            options={
                "verbose_name": "жанр",
                "verbose_name_plural": "жанры",
            },
        ),
        migrations.CreateModel(
            name="Track",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="название трека"),
                ),
                (
                    "artist",
                    models.CharField(max_length=100, verbose_name="исполнитель"),
                ),
                (
                    "genre",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="graph_recsys.genre",
                        verbose_name="жанр",
                    ),
                ),
                (
                    "listeners",
                    models.ManyToManyField(
                        to=settings.AUTH_USER_MODEL, verbose_name="слушатели"
                    ),
                ),
            ],
            options={
                "verbose_name": "трек",
                "verbose_name_plural": "треки",
            },
        ),
    ]
