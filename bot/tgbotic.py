import os
import sys

import django
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.utils import executor

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
    if len(text_l) != 4:
        await message.answer("Неверный формат команды. Используйте: /register <username> <phone> <email> <password>")
        return

    username, phone, password = text_l[1], text_l[2], text_l[3]

    register_api_view = RegisterAPIView()
    # Проверьте, что create_user является синхронной функцией. Если нет, вызывайте её напрямую
    await register_api_view.create_user(username, phone, message.chat.id, password)
    await message.answer("Регистрация завершена!")


@dp.message_handler(commands=['set_habit'], state='*')
async def make_habit(message: Message):
    """ Команда для создания привычки"""
    text_l = message.text.split()
    if len(text_l) != 13:
        await message.answer(
            "Неверный формат команды. Используйте: /set_habit <title> <user_id> <place> <time> <action> <is_useful> <is_pleasant> <frequency> <duration> <is_published> <related_habit> <reward>")
        return

    title, user_id, place, time, action, is_useful, is_pleasant, frequency, duration, is_published, related_habit, reward = \
    text_l[1], int(text_l[2]), text_l[3], text_l[4], text_l[5], text_l[6], text_l[7], text_l[8], text_l[9], text_l[10], \
    text_l[11], text_l[12]

    habit_create_view = HabitCreateView()
    # Проверьте, что post является синхронной функцией. Если нет, вызывайте её напрямую
    await habit_create_view.post(title, user_id, place, time, action, is_useful, is_pleasant, frequency, duration,
                                 is_published, related_habit, reward)
    await message.answer("Привычка успешно создана!")


@dp.message_handler(commands=['list_habits'], state='*')
async def get_all_habits(message: Message):
    """ Команда для получения списка привычек"""
    habit_view_set = HabitViewSet()
    # Проверьте, что get_queryset является синхронной функцией. Если нет, вызывайте её напрямую
    habits = await habit_view_set.get_queryset()
    habits_list = "\n".join([str(habit) for habit in habits])
    await message.answer(habits_list)


@dp.message_handler(commands=['edit_habit'], state='*')
async def edit_habit(message: Message):
    """ Команда для редактирования привычки"""
    habit_update_api_view = HabitUpdateAPIView()
    # Проверьте, что put является синхронной функцией. Если нет, вызывайте её напрямую
    await habit_update_api_view.put()
    await message.answer("Привычка отредактирована!")


@dp.message_handler(commands=['delete_habit'], state='*')
async def delete_habit(message: Message):
    """ Команда для удаления привычки """
    habit_destroy_api_view = HabitDestroyAPIView()
    # Проверьте, что delete является синхронной функцией. Если нет, вызывайте её напрямую
    await habit_destroy_api_view.delete()
    await message.answer("Привычка удалена!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
