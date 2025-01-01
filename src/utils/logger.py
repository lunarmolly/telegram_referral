"""
Модуль для настройки логирования в проекте.

Обеспечивает запись логов в файл и вывод их в консоль.

Функции:
- setup_logger: создает и настраивает логгер с заданными параметрами.

Логгер 'main_logger' используется как основной логгер приложения.
"""

import logging
import os

# Уровни логирования
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
LOG_FILE = os.path.join(LOG_DIR, "bot.log")

# Убедимся, что директория для логов существует
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Настраивает логгер с указанным именем и уровнем логирования."""
    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Формат для логов
    formatter = logging.Formatter(LOG_FORMAT)

    # Обработчик для записи в файл
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Главный логгер приложения
main_logger = setup_logger("main", logging.DEBUG)
