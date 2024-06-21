from datetime import datetime
import os
import sys
from django_setup import setup_django

setup_django()

# Корневой каталог проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import timedelta, timezone
from users.views import RegisterAPIView
from users.models import User
from main.models import Habit
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.utils import executor
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from config import settings
from main.worker import send_telegram_reminder, schedule_daily_reminders

# Настройка бота
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
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
    await register_api_view.create_user(username, phone, message.chat.id, password)
    await message.answer("Регистрация завершена!")


@dp.message_handler(commands=['set_habit'], state='*')
async def make_habit(message: Message):
    text = message.text.replace('/set_habit', '').strip()
    text_l = text.split()

    if len(text_l) != 11:
        await message.answer(
            "Неверный формат команды. Используйте: "
            "/set_habit <title> <place> <time> <action> "
            "<is_useful> <is_pleasant> <frequency> <duration> "
            "<is_published> <related_habit> <reward>"
        )
        return

    title = text_l[0]
    place = text_l[1]
    time = text_l[2]
    action = text_l[3]
    is_useful = text_l[4].lower() == 'да'
    is_pleasant = text_l[5].lower() == 'да'
    frequency = text_l[6]

    # Преобразуем строку duration в timedelta
    try:
        duration = timedelta(hours=int(text_l[7].split(':')[0]), minutes=int(text_l[7].split(':')[1]))
    except ValueError:
        await message.answer("Неверный формат продолжительности. Используйте формат HH:MM.")
        return

    is_published = text_l[8].lower() == 'опубликована'

    related_habit_title = text_l[9]
    reward = ' '.join(text_l[10:])  # Объединяем оставшиеся элементы в строку

    # Пытаемся найти связанную привычку по названию
    if related_habit_title.lower() == 'нет':
        related_habit = None
    else:
        try:
            # Используйте sync_to_async для вызова Habit.objects.get
            related_habit = await sync_to_async(Habit.objects.get)(title=related_habit_title)
        except ObjectDoesNotExist:
            await message.answer(f"Привычка '{related_habit_title}' не найдена.")
            return

    # Пытаемся найти пользователя по bot_id
    user_bot_id = message.from_user.id
    try:
        # Используйте sync_to_async для вызова User.objects.get
        user = await sync_to_async(User.objects.get)(bot_id=user_bot_id)
    except ObjectDoesNotExist:
        await message.answer(f"Пользователь с bot_id {user_bot_id} не найден.")
        return

    # Создаем новую привычку
    new_habit = await sync_to_async(Habit.objects.create)(
        title=title,
        bot_id=user.bot_id,
        place=place,
        time=time,
        action=action,
        is_useful=is_useful,
        is_pleasant=is_pleasant,
        frequency=frequency,
        duration=duration,
        is_published=is_published,
        related_habit=related_habit,
        reward=reward
    )

    remind_time = datetime.strptime(time, '%H:%M')  # Преобразование времени из строки в объект datetime
    now = datetime.now()
    today = datetime(now.year, now.month, now.day, remind_time.hour, remind_time.minute)
    if now > today:
        remind_time = today + timedelta(days=1)
    else:
        remind_time = today

    schedule_daily_reminders.apply_async((new_habit.id,), eta=remind_time)

    await message.answer(f"Привычка '{title}' успешно создана!")


@dp.message_handler(commands=['list_habits'], state='*')
async def get_all_habits(message: Message):
    """ Команда для получения списка привычек """
    user_bot_id = message.from_user.id

    try:
        user = await sync_to_async(User.objects.get)(bot_id=user_bot_id)
    except User.DoesNotExist:
        await message.answer(f"Пользователь с bot_id {user_bot_id} не найден.")
        return

    try:
        habits = await sync_to_async(list)(Habit.objects.filter(bot_id=user.bot_id))
    except Habit.DoesNotExist:
        await message.answer(f"Привычки для пользователя с bot_id {user_bot_id} не найдены.")
        return

    habits_list = "\n".join([str(habit) for habit in habits])
    await message.answer(habits_list)


@dp.message_handler(commands=['edit_habit'], state='*')
async def edit_habit(message: Message):
    """ Команда для редактирования привычки"""
    # Получаем текст после команды /edit_habit
    text = message.text.replace('/edit_habit', '').strip()

    # Проверяем, что сообщение не пустое после удаления команды
    if not text:
        await message.answer("Неверный формат команды. Используйте: /edit_habit id=<id> <поля для изменения>")
        return

    # Извлекаем id привычки из сообщения
    habit_id = None
    try:
        habit_id = int(text.split()[0].split('=')[1])  # Получаем id из сообщения
    except (IndexError, ValueError):
        await message.answer("Неверный формат id. Используйте: /edit_habit id=<id> <поля для изменения>")
        return

    # Ищем привычку по id
    try:
        habit = await sync_to_async(Habit.objects.get)(id=habit_id)
    except Habit.DoesNotExist:
        await message.answer(f"Привычка с id={habit_id} не найдена.")
        return

    # Обрабатываем изменения полей привычки
    updates = {}
    fields = text.split()[1:]  # Оставшиеся части сообщения - поля для изменения

    for field in fields:
        try:
            key, value = field.split('=')
            updates[key.strip()] = value.strip()
        except ValueError:
            await message.answer(f"Неверный формат поля '{field}'. Используйте: поле=значение")
            return

    # Применяем изменения к привычке
    for key, value in updates.items():
        if key == 'id':  # Нельзя изменять id привычки
            continue
        elif hasattr(habit, key):
            setattr(habit, key, value)
        else:
            await message.answer(f"Поле '{key}' не существует в модели привычки.")
            return

    # Сохраняем обновленную привычку
    await sync_to_async(habit.save)()

    await message.answer(f"Привычка с id={habit_id} успешно отредактирована!")


@dp.message_handler(commands=['delete_habit'], state='*')
async def delete_habit(message: Message):
    """ Команда для удаления привычки """
    # Получаем текст после команды /delete_habit
    text = message.text.replace('/delete_habit', '').strip()

    # Проверяем, что сообщение не пустое после удаления команды
    if not text:
        await message.answer("Неверный формат команды. Используйте: /delete_habit id=<id>")
        return

    # Извлекаем id привычки из сообщения
    habit_id = None
    try:
        habit_id = int(text.split('=')[1])  # Получаем id из сообщения
    except (IndexError, ValueError):
        await message.answer("Неверный формат id. Используйте: /delete_habit id=<id>")
        return

    # Пытаемся найти привычку по id
    try:
        habit = await sync_to_async(Habit.objects.get)(id=habit_id)
    except Habit.DoesNotExist:
        await message.answer(f"Привычка с id={habit_id} не найдена.")
        return

    # Удаляем привычку
    await sync_to_async(habit.delete)()

    await message.answer(f"Привычка с id={habit_id} успешно удалена!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
