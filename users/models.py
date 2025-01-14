from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""

    username = None

    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите email"
    )

    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        help_text="Введите телефон",
        blank=True,
        null=True,
    )
    country = models.CharField(
        max_length=150,
        verbose_name="Город",
        help_text="Введите город",
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        help_text="Загрузите аватар",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
