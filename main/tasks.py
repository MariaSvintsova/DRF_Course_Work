from celery import shared_task
from django.conf import settings
import telegram

from users.models import User
from .models import Habit
from datetime import datetime

bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)

@shared_task
def send_telegram_reminder(obj):
    try:
        habit = Habit.objects.get(id=obj.id)
        message = f"Напоминание: пора выполнять привычку '{habit.title}' в {habit.time}"
        bot.send_message(chat_id=User.objects.get(id=obj["user"]).bot_id, text=message)
    except Habit.DoesNotExist:
        pass

@shared_task
def schedule_daily_reminders():
    habits = Habit.objects.filter(is_published=True)
    for habit in habits:
        habit_time = datetime.combine(datetime.now().date(), habit.time)
        send_telegram_reminder.apply_async((habit.id,), eta=habit_time)
