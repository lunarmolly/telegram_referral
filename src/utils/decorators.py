"""
Модуль с декораторами для проекта.

Содержит:
- Декоратор для логирования выполнения функций.
- Декоратор retry для повторной попытки выполнения функции при ошибке.
"""

import time
from functools import wraps
from src.utils.logger import main_logger

def log_execution(level="info"):
    """
    Декоратор для логирования выполнения функций.

    :param level: Уровень логирования (info, debug, warning, error, critical).
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log_func = getattr(main_logger, level, main_logger.info)
            log_func(f"Вызов функции {func.__name__} с аргументами: {args}, {kwargs}")
            try:
                result = func(*args, **kwargs)
                log_func(f"Функция {func.__name__} успешно выполнена.")
                return result
            except Exception as e:
                main_logger.error(f"Ошибка в функции {func.__name__}: {e}")
                raise
        return wrapper
    return decorator

def retry(retries=3, delay=2):
    """
    Декоратор для повторной попытки выполнения функции при возникновении исключений.

    :param retries: Количество попыток.
    :param delay: Задержка между попытками в секундах.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    main_logger.warning(f"Ошибка: {e} в {func.__name__}. Попытка {attempts} из {retries}.")
                    if attempts == retries:
                        main_logger.error(f"Функция {func.__name__} не выполнена после {retries} попыток.")
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator
