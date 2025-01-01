from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.utils.decorators import log_execution


@log_execution()
def get_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Профиль")
    kb.button(text="Сделать заказ")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)