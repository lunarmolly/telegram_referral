"""
Основной модуль для запуска Telegram-бота telegram_referral_bot.

Этот модуль отвечает за:
- Инициализацию бота и диспетчера.
- Регистрацию всех обработчиков.
- Запуск процесса поллинга.
"""

import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

from src.bot import handlers
from src.utils.logger import main_logger

async def main():
    """
    Основная точка входа для запуска бота.
    """
    main_logger.info("Запуск бота")
    # Загрузка переменных окружения
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")

    if not bot_token:
        raise ValueError("Не удалось найти токен бота BOT_TOKEN. Проверьте файл .env")

    if not os.getenv("BOT_LINK"):
        raise ValueError("Не удалось найти ссылку на бота BOT_LINK. Проверьте файл .env")

    bot = Bot(token=bot_token)
    dp = Dispatcher()

    # Регистрация роутера с обработчиками
    dp.include_router(handlers.router)

    # Пропуск накопленных входящих
    await bot.delete_webhook(drop_pending_updates=True)

    # Запуск поллинга
    try:
        main_logger.info("Бот запущен и готов к работе")
        await dp.start_polling(bot)
    except Exception as e:
        main_logger.error(f"Ошибка запуска бота: {str(e)}")
    finally:
        await bot.session.close()
        main_logger.info("Бот остановлен")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        main_logger.critical(f"Критическая ошибка при запуске бота: {str(e)}")
