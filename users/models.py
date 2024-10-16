from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    first_name = models.CharField(
        max_length=200, verbose_name="имя", help_text="Укажите имя"
    )
    last_name = models.CharField(
        max_length=200, verbose_name="фамилия", help_text="Укажите фамилию"
    )
    email = models.EmailField(
        unique=True, verbose_name="email", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="телефон",
        help_text="Укажите номер телефона",
        **NULLABLE
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="аватар",
        help_text="Загрузите аватар",
        **NULLABLE
    )
    city = models.CharField(
        max_length=200, verbose_name="город", help_text="Укажите Ваш город", **NULLABLE
    )
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.email
