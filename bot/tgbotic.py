import os
import sys

import django
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.utils import executor
from asgiref.sync import sync_to_async

from main.models import Habit
from users.models import User

# Установка переменной окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
except Exception as e:
    print(f"Failed to setup Django: {e}")
    raise
# Корневой каталог проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Настройка Django
try:
    django.setup()
except Exception as e:
    print(f"Failed to setup Django: {e}")
    sys.exit(1)

# Импорт Django модуля после настройки Django
from main.views import HabitCreateView, HabitUpdateAPIView, HabitDestroyAPIView, HabitViewSet
from users.views import RegisterAPIView

# Настройка бота
bot = Bot(token="7309181886:AAGL8ologK1csMb8TaTCQZ65KxyoNWvzuy8")
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'], state="*")
async def start_command(message: Message) -> None:
    """ Стартовая команда начала разговора """
    text = """
    Привет! Команды бота:
    /register - регистрация
    /set_habit - создание привычки
    /edit_habit - редактирование привычки
    /delete_habit - удаление привычки
    /list_habits - список привычек
    """
    await bot.send_message(chat_id=message.chat.id, text=text)

@dp.message_handler(commands=['register'], state='*')
async def register(message: Message):
    """ Команда для регистрации пользователя"""
    text_l = message.text.split()
    if len(text_l) != 5:
        await message.answer("Неверный формат команды. Используйте: /register <username> <phone> <email> <password>")

    username, phone, email, password = text_l[1], text_l[2], text_l[3], text_l[4]
    await sync_to_async(RegisterAPIView().create_user)(username, phone, email, message.from_user.id)
    await message.answer("Регистрация завершена!")

@dp.message_handler(commands=['set_habit'], state='*')
async def make_habit(message: Message):
    """ Команда для создания привычки"""
    text_l = message.text.split()
    if len(text_l) != 13:
        await message.answer(
            "Неверный формат команды. Используйте: /set_habit <title> <user_id> <place> <time> <action> <is_useful> <is_pleasant> <frequency> <duration> <is_published> <related_habit> <reward>")
        return

    title, user_id, place, time, action, is_useful, is_pleasant, frequency, duration, is_published, related_habit, reward = text_l[
                                                                                                                            1:]

    try:
        user = await sync_to_async(User.objects.get)(id=user_id)
        habit = await sync_to_async(Habit.objects.create)(
            title=title, user=user, place=place, time=time, action=action, is_useful=is_useful, is_pleasant=is_pleasant,
            frequency=frequency, duration=duration, is_published=is_published, related_habit=related_habit,
            reward=reward
        )
        await message.answer("Привычка успешно создана!")
    except User.DoesNotExist:
        await message.answer(f"Пользователь с ID {user_id} не найден.")
    except Exception as e:
        await message.answer(f"Ошибка при создании привычки: {e}")

@dp.message_handler(commands=['list_habits'], state='*')
async def get_all_habits(message: Message):
    """ Команда для получения списка привычек"""
    habits = await sync_to_async(HabitViewSet().get_queryset)()
    habits_list = "\n".join([str(habit) for habit in habits])
    await message.answer(habits_list)


@dp.message_handler(commands=['edit_habit'], state='*')
async def edit_habit(message: Message):
    """ Команда для редактирования привычки"""
    await sync_to_async(HabitUpdateAPIView)()
    await message.answer("Привычка отредактирована!")

@dp.message_handler(commands=['delete_habit'], state='*')
async def delete_habit(message: Message):
    """ Команда для удаления привычки """
    await sync_to_async(HabitDestroyAPIView)()
    await message.answer("Привычка удалена!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
