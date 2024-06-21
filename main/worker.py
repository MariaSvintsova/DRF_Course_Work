# main/tasks.py
from celery import shared_task
from django.conf import settings
from aiogram import Bot, Dispatcher
from datetime import datetime, timedelta
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@shared_task
def send_telegram_reminder(habit_id):
    from users.models import User
    from .models import Habit
    """Reminder for user in tg_bot"""
    print(2)
    try:
        habit = Habit.objects.get(id=habit_id)
        user = User.objects.get(id=habit.user.id)
        message = f"Напоминание: пора выполнять привычку '{habit.title}' в {habit.time}"
        bot.send_message(chat_id=user.bot_id, text=message)
    except Habit.DoesNotExist:
        pass
    except User.DoesNotExist:
        pass

@shared_task
def schedule_daily_reminders(habit_id):
    """Task to schedule daily reminders for published habits."""
    print(1)
    send_telegram_reminder.apply_async((habit_id,), eta=datetime.now() + timedelta(seconds=60))
