from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """
    Модель пользователя
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="почта")
    avatar = models.ImageField(
        upload_to="users/avatars", verbose_name="аватар", **NULLABLE
    )
    token = models.CharField(max_length=100, verbose_name="token", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email