from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}

class User(AbstractUser):
    username = models.CharField(max_length=250, verbose_name='Имя')
    phone = models.CharField(max_length=100, verbose_name='Номер телефона', **NULLABLE)
    email = models.CharField(max_length=100, verbose_name='Email пользователя', **NULLABLE)
    password = models.CharField(max_length=100, verbose_name='Пароль пользователя')
    bot_id = models.BigIntegerField(verbose_name='ТG_id пользователя', unique=True,  **NULLABLE)

    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'