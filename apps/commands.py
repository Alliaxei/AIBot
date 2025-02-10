from aiogram import Bot
from aiogram.types import BotCommand


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Перезапустить бота'),
        BotCommand(command='help', description='Помощь'),
    ]
    await bot.set_my_commands(commands)
