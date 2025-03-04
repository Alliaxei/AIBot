import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from apps.handlers.commands import router as commands_router
from apps.handlers.callbacks import router as callbacks_router
from apps.handlers.states import router as states_router
from apps.commands import set_bot_commands
from apps.scheduler import start_scheduler


async def main():
    load_dotenv('.env')
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(commands_router)
    dp.include_router(callbacks_router)
    dp.include_router(states_router)


    try:
        start_scheduler()

        await set_bot_commands(bot)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")