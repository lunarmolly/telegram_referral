"""
Модуль для работы с JSON базой данных в telegram_referral_bot.

Содержит функции для чтения, записи и обновления данных в JSON-файле.
Формат данных:
{
    "<user_id>": {
        "telegram_id": <int>,
        "referred_by": "<referrer_user_id>"
    },
    ...
}
"""

import json
import os
from src.utils.decorators import log_execution
from filelock import FileLock, Timeout
from src.utils.logger import main_logger

# Путь к базе данных
DB_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "data.json")
LOCK_FILE_PATH = f"{DB_FILE_PATH}.lock"

def validate_user_data(user_id: str, telegram_id: int, referred_by: str = None) -> None:
    """
    Валидирует данные пользователя перед записью в базу данных.

    :param user_id: Уникальный ID пользователя.
    :param telegram_id: Telegram ID пользователя.
    :param referred_by: ID пользователя, который пригласил этого пользователя.
    :raises ValueError: Если данные некорректны.
    """
    if not isinstance(user_id, str) or not user_id:
        raise ValueError("user_id должен быть непустой строкой.")
    if not isinstance(telegram_id, int) or telegram_id <= 0:
        raise ValueError("telegram_id должен быть положительным числом.")
    if referred_by is not None and (not isinstance(referred_by, str) or not referred_by):
        raise ValueError("referred_by должен быть строкой или None.")

@log_execution(level="info")
def read_json() -> dict:
    """
    Читает данные из JSON файла.

    :return: Словарь с данными.
    """
    if not os.path.exists(DB_FILE_PATH):
        return {}

    try:
        with FileLock(LOCK_FILE_PATH, timeout=10):
            with open(DB_FILE_PATH, "r", encoding="utf-8") as file:
                return json.load(file)
    except Timeout:
        main_logger.error("Не удалось получить доступ к файлу для чтения: превышено время ожидания.")
        raise

@log_execution(level="info")
def write_json(data: dict) -> None:
    """
    Записывает данные в JSON файл.

    :param data: Словарь с данными для записи.
    """
    os.makedirs(os.path.dirname(DB_FILE_PATH), exist_ok=True)
    try:
        with FileLock(LOCK_FILE_PATH, timeout=10):
            with open(DB_FILE_PATH, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
    except Timeout:
        main_logger.error("Не удалось получить доступ к файлу для записи: превышено время ожидания.")
        raise

@log_execution(level="info")
def add_user(user_id: str, telegram_id: int, referred_by: str = None) -> None:
    """
    Добавляет нового пользователя в базу данных.

    :param user_id: Уникальный ID пользователя.
    :param telegram_id: Telegram ID пользователя.
    :param referred_by: ID пользователя, который пригласил этого пользователя.
    """
    validate_user_data(user_id, telegram_id, referred_by)
    data = read_json()
    if user_id not in data:
        data[user_id] = {
            "telegram_id": telegram_id,
            "referred_by": referred_by
        }
        write_json(data)

@log_execution(level="info")
def get_referral_count(user_id: str) -> int:
    """
    Возвращает количество рефералов для указанного пользователя.

    :param user_id: ID пользователя.
    :return: Количество рефералов.
    """
    data = read_json()
    return sum(1 for user in data.values() if user.get("referred_by") == user_id)

@log_execution(level="info")
def delete_user(user_id: str) -> None:
    """
    Удаляет пользователя из базы данных.

    :param user_id: ID пользователя для удаления.
    """
    data = read_json()
    if user_id in data:
        del data[user_id]
        write_json(data)
