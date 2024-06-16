from django.db import models

from django.db import models


from main.validators import PleasantHabitsValidator, RelatedHabitsValidator, DurationValidator, \
    RewardAndRelatedHabitsValidator
from users.models import User

NULLABLE = {'blank': True, 'null': True}

FREQUENCY_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
    ]

class Habit(models.Model):
    """ Model of habit """

    title = models.CharField(max_length=255, verbose_name='Название привычки')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits', verbose_name='Cоздатель привычки')
    place = models.CharField(max_length=255, verbose_name='Место, в котором необходимо выполнять привычку')
    time = models.TimeField(verbose_name='Время, когда необходимо выполнять привычку')
    action = models.CharField(max_length=50, verbose_name='Действие, которое представляет собой привычка')
    is_useful = models.BooleanField(default=True, verbose_name='Признак полезной привычки', **NULLABLE)
    is_pleasant = models.BooleanField(default=True, verbose_name='привычка, которую можно привязать к выполнению полезной привычки')
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily', verbose_name='Периодичность')
    duration = models.DurationField(help_text='Продолжительность выполнения привычки')
    is_published = models.BooleanField(default=False, verbose_name='Признак публичности')
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE, **NULLABLE, verbose_name='Связанная привычка', default=None)
    reward = models.TextField(verbose_name='Вознаграждение', **NULLABLE,  default=None)


    def __str__(self):
        return f'{self.action} в {self.time} в {self.place}'


    def clean(self):

        RewardAndRelatedHabitsValidator()(self)
        DurationValidator()(self)
        RelatedHabitsValidator()(self)
        PleasantHabitsValidator()(self)


    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Создание привычки'
        verbose_name_plural = 'Создание привычек'


