from django.db import models
from users.models import User
NULLABLE = {"null": True, "blank": True}

class Genre(models.Model):
    """
    модель жанра
    """
    name = models.CharField(max_length=100, verbose_name='название жанра')

    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "жанры"

    def __str__(self):
        return self.name


class Track(models.Model):
    """
    модель трека
    """
    name = models.CharField(max_length=100, verbose_name='название трека')
    artist = models.CharField(max_length=100, verbose_name='исполнитель')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name='жанр')
    listeners = models.ManyToManyField(User, verbose_name='слушатели')

    class Meta:
        verbose_name = "трек"
        verbose_name_plural = "треки"

    def __str__(self):
        return f'{self.artist} - {self.name} genre: {self.genre}'

class Prefer(models.Model):
    '''
    модель предпочтений
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='фанат', **NULLABLE)
    genres = models.ManyToManyField(Genre, verbose_name='жанры', related_name='prefer')

    class Meta:
        verbose_name = "предпочтение"
        verbose_name_plural = "предпочтения"

    def __str__(self):
        return f'{self.id}'
