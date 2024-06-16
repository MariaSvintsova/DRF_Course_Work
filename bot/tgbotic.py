import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.utils import executor
from asgiref.sync import sync_to_async

# Установите переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Добавьте корневой каталог проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Настройка Django
import django
django.setup()

# Импортируйте Django модули после настройки Django
from main.views import HabitCreateView, HabitUpdateAPIView, HabitDestroyAPIView, HabitViewSet
from users.views import RegisterAPIView

# Настройка бота
bot = Bot(token="YOUR_TELEGRAM_BOT_TOKEN")
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'], state="*")
async def start_command(message: Message) -> None:
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
    text_l = message.text.split()
    if len(text_l) != 5:
        await message.answer("Неверный формат команды. Используйте: /register <username> <phone> <email> <password>")
        return

    username, phone, email, password = text_l[1], text_l[2], text_l[3], text_l[4]
    await sync_to_async(RegisterAPIView().create_user)(username, phone, email, message.from_user.id)
    await message.answer("Регистрация завершена!")

@dp.message_handler(commands=['set_habit'], state='*')
async def make_habit(message: Message):
    text_l = message.text.split()
    if len(text_l) != 13:
        await message.answer("Неверный формат команды. Используйте: /set_habit <title> <user_id> <place> <time> <action> <is_useful> <is_pleasant> <frequency> <duration> <is_published> <related_habit> <reward>")
        return

    title, user_id, place, time, action, is_useful, is_pleasant, frequency, duration, is_published, related_habit, reward = text_l[1], int(text_l[2]), text_l[3], text_l[4], text_l[5], text_l[6], text_l[7], text_l[8], text_l[9], text_l[10], text_l[11], text_l[12]

    await sync_to_async(HabitCreateView().post)(title, user_id, place, time, action, is_useful, is_pleasant, frequency, duration, is_published, related_habit, reward)
    await message.answer("Привычка успешно создана!")

@dp.message_handler(commands=['list_habits'], state='*')
async def get_all_habits(message: Message):
    habits = await sync_to_async(HabitViewSet().get_queryset)()
    # Преобразуем список привычек в строку для отправки в сообщении
    habits_list = "\n".join([str(habit) for habit in habits])
    await message.answer(habits_list)

@dp.message_handler(commands=['edit_habit'], state='*')
async def edit_habit(message: Message):
    # Реализация логики редактирования привычки
    await sync_to_async(HabitUpdateAPIView)()
    await message.answer("Привычка отредактирована!")

@dp.message_handler(commands=['delete_habit'], state='*')
async def delete_habit(message: Message):
    # Реализация логики удаления привычки
    await sync_to_async(HabitDestroyAPIView)()
    await message.answer("Привычка удалена!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
