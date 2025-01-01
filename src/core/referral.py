"""
Модуль для работы с реферальной системой в.

Этот модуль реализует:
- Генерацию уникальных реферальных ссылок.
- Расчет скидок на основе количества приглашенных пользователей.
"""

from src.utils.decorators import log_execution
from dotenv import load_dotenv
import os

@log_execution(level="info")
def generate_referral_link(telegram_id: int) -> str:
    """
    Генерация уникальной реферальной ссылки для пользователя.

    :param telegram_id: Уникальный Telegram ID пользователя.
    :return: Реферальная ссылка.
    """
    load_dotenv()
    bot_link = os.getenv("BOT_LINK")

    return f"{bot_link}?start={telegram_id}"

@log_execution(level="info")
def get_discount(referrals_count: int) -> str:
    """
    Расчет текущей скидки для пользователя на основе его реферальной активности.

    :param referrals_count: Количество рефералов пользователя.
    :return: Скидки на заказы в виде строки.
    """
    discount_steps = [10, 30, 50, 70]  # Скидки за 1, 2, 3, 4 рефералов

    discounts = [70] * (referrals_count // 4)
    if referrals_count % 4 != 0:
        discounts.append(discount_steps[referrals_count % 4 - 1])

    # Формируем строку со списком скидок
    discounts_message = ""
    for i, discount in enumerate(discounts):
        if len(discounts_message) == 0:  # Первая скидка всегда "на следующий заказ"
            discounts_message += f"Скидка на следующий заказ: {discount}%\n"
        else:
            discounts_message += f"Скидка на {i + 1} заказ: {discount}%\n"
    if len(discounts_message) == 0:
        discounts_message += f"Скидка на следующий заказ: 0%"

    return discounts_message.strip()

