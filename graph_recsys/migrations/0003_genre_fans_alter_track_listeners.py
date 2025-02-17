# Generated by Django 5.1.3 on 2024-11-08 07:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("graph_recsys", "0002_rename_genre_name_genre_name_alter_track_listeners"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="genre",
            name="fans",
            field=models.ManyToManyField(
                to=settings.AUTH_USER_MODEL, verbose_name="фанаты"
            ),
        ),
        migrations.AlterField(
            model_name="track",
            name="listeners",
            field=models.ManyToManyField(
                to=settings.AUTH_USER_MODEL, verbose_name="слушатели"
            ),
        ),
    ]
