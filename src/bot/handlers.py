"""
Модуль для обработки команд бота.

Содержит хэндлеры для основных команд и кнопок меню.
"""

from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove
from src.bot.keyboards import get_menu_kb
from src.utils.decorators import log_execution
from src.db.json_db import add_user, read_json
from src.core.referral import generate_referral_link, get_discount

router = Router()

@router.message(Command("start"))
@log_execution()
async def start_handler(message: types.Message, command: Command):
    """Обработка команды /start."""
    user_id = str(message.from_user.id)
    telegram_id = message.from_user.id

    # Проверка параметра start в ссылке
    referred_by = None
    if command.args:
        referred_by = command.args

    # Проверка, зарегистрирован ли пользователь
    data = read_json()
    if user_id in data:
        await message.answer(
            "Вы уже зарегистрированы в системе.",
            reply_markup=get_menu_kb()
        )
        return

    # Регистрация пользователя в базе данных
    add_user(user_id, telegram_id, referred_by)

    # Приветственное сообщение
    await message.answer(
        f"Привет, {message.from_user.first_name}! 🎉\n"
        f"Вы успешно зарегистрированы.\n"
        f"Ваша реферальная ссылка: {generate_referral_link(telegram_id)}\n"
        f"Делитесь ей с друзьями, чтобы получать бонусы!",
        reply_markup=get_menu_kb()
    )


@router.message(F.text == "Профиль")
@log_execution()
async def profile_handler(message: types.Message):
    """Обработка нажатия кнопки 'Профиль'."""
    user_id = str(message.from_user.id)
    data = read_json()

    if user_id in data:
        user_data = data[user_id]
        referred_by = user_data.get("referred_by", "Не указано")
        referrals_count = sum(1 for user in data.values() if user.get("referred_by") == user_id)
        discount = get_discount(referrals_count)

        await message.answer(
            f"Ваш профиль:\n"
            f"ID: {user_id}\n"
            f"Реферальная ссылка: {generate_referral_link(user_data['telegram_id'])}\n"
            f"Количество приглашенных друзей: {referrals_count}\n"
            f"Скидка: \n{discount}",
            reply_markup=get_menu_kb()
        )
    else:
        await message.answer("Ваш профиль не найден. Используйте /start для регистрации.", reply_markup=ReplyKeyboardRemove())

@router.message(F.text == "Сделать заказ")
@log_execution()
async def order_handler(message: types.Message):
    """Обработка нажатия кнопки 'Сделать заказ'."""
    order_message = (
        "Вы хотите сделать заказ? После перехода по следующей ссылке "
        "[сделать заказ](https://t.me/m/oYBDs3KZOTdi) откроется личный чат со мной.\n"
        "Если у вас есть вопросы, напишите мне прямо в личном чате!"
    )
    await message.answer(order_message, parse_mode="Markdown", reply_markup=get_menu_kb())
