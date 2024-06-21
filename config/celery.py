from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery
app = Celery('DRF_CourseWork')

# Загрузка настроек из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов worker.py в приложениях Django
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Настройка периодических задач
from main.worker import schedule_daily_reminders

# Настройка периодических задач
app.conf.beat_schedule = {
    'schedule-daily-reminders': {
        'task': 'main.tasks.schedule_daily_reminders',
        'schedule': crontab(hour=0, minute=0),  # Запуск каждый день в полночь
    },
}

# bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
# from main.models import Habit
# @shared_task
# def send_telegram_reminder(habit_id):
#     try:
#         habit = Habit.objects.get(id=habit_id)
#         chat_id = habit.user.bot_id
#         if chat_id:
#             message = f"Напоминание: пора выполнять привычку '{habit.title}' в {habit.time}"
#             bot.send_message(chat_id=chat_id, text=message)
#     except Habit.DoesNotExist:
#         pass
