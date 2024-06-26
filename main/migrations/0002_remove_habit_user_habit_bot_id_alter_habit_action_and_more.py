# Generated by Django 5.0.6 on 2024-06-19 16:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habit',
            name='user',
        ),
        migrations.AddField(
            model_name='habit',
            name='bot_id',
            field=models.BigIntegerField(blank=True, null=True, unique=True, verbose_name='ТG_id пользователя'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='action',
            field=models.CharField(max_length=50, verbose_name='Действие, которое представляет собой привычку'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='frequency',
            field=models.CharField(choices=[('daily', 'Ежедневно'), ('weekly', 'Еженедельно'), ('monthly', 'Ежемесячно')], default='daily', max_length=10, verbose_name='Периодичность'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='is_pleasant',
            field=models.BooleanField(default=True, verbose_name='Привычка, которую можно привязать к выполнению полезной привычки'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='is_useful',
            field=models.BooleanField(default=True, verbose_name='Признак полезной привычки'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='related_habit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.habit', verbose_name='Связанная привычка'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='reward',
            field=models.TextField(blank=True, null=True, verbose_name='Вознаграждение'),
        ),
    ]
