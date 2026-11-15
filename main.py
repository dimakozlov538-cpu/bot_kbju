import asyncio
import logging
import socket

from aiohttp import TCPConnector
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.exceptions import TelegramNetworkError

from config import BOT_TOKEN
from handlers.calculator import router as calc_router

logging.basicConfig(level=logging.INFO)


class IPv4AiohttpSession(AiohttpSession):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._connector_init["family"] = socket.AF_INET


async def main():
    session = IPv4AiohttpSession(timeout=60)
    
    bot = Bot(token=BOT_TOKEN, session=session)
    dp = Dispatcher()
    dp.include_router(calc_router)
    
    while True:
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot)
        except TelegramNetworkError as e:
            logging.warning(f"Сетевой сбой: {e}. Повторная попытка через 5 секунд...")
            await asyncio.sleep(5)
        except Exception as e:
            logging.error(f"Критическая ошибка: {e}")
            break
        finally:
            await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен вручную.")
