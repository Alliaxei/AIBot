import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
# from aiogram.dispatcher import router
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
# from handlers.handler_states import router

from apps.handlers.handler_commands import router as commands_router
from apps.handlers.handler_callbacks import router as callbacks_router
from apps.handlers.handler_states import router as states_router

from apps.commands import set_bot_commands

async def main():
    load_dotenv('.env')
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher(storage=MemoryStorage()) # Стирает данные диспетчера после перезапуска, все данные, которые не хранятся в БД
    # dp.include_router(router)

    dp.include_router(commands_router)
    dp.include_router(callbacks_router)
    dp.include_router(states_router)

    try:
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