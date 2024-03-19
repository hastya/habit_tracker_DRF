from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

NULLABLE = {'null': True, 'blank': True}


class Habit(models.Model):

    PERIODICITY_CHOICES = [
        (1, 'Ежедневно'),
        (2, 'Еженедельно')
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user', verbose_name='Пользователь')
    place = models.CharField(max_length=50, verbose_name='Место')
    # time = models.TimeField(verbose_name='Время')
    time = models.TimeField(default=timezone.now, verbose_name="Время начала привычки")
    action = models.CharField(max_length=300, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Признак приятности')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, **NULLABLE, related_name='main_habit', verbose_name='Связанная привычка')
    periodicity = models.PositiveIntegerField(default=1, choices=PERIODICITY_CHOICES, verbose_name='Периодичность')
    reward = models.CharField(max_length=300, **NULLABLE, verbose_name='Вознаграждение')
    duration = models.DurationField(verbose_name='Длительность выполнения')
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')
    objects = models.Manager()

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ('pk',)
