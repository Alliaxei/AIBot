from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from apps.keyboards import keyboards as kb
from apps.database import requests

router = Router()

@router.message(Command('start'))
async def start_handler(message: Message):
    await requests.set_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    await message.answer("🌟 Привет! Рад тебя видеть! 🎉\nНаш бот умеет генерировать изображения, видео и тексты. Выбирай, что тебе нужно, и давай начнем! 👇😊",
                         reply_markup=kb.main)

@router.message(Command('help'))
async def help_handler(message: Message):
    await message.answer(
        "🤖 *О боте*\n"
        "Этот бот умеет генерировать *текст*, *изображения* и *видео* по текстовому описанию! 🖼️🎥✍️\n\n"
        "💰 *Система кредитов*\n"
        "— Каждая генерация требует кредиты.\n"
        "— Ежедневно начисляются *бесплатные кредиты*.\n"
        "— Можно пополнить баланс через *ЮМани*.\n\n"
        "📌 *Как пользоваться?*\n"
        "Выбирай нужную функцию в меню и следуй инструкциям! 🚀\n\n"
        "🔄 *Перезапуск бота*\n"
        "Если что-то пошло не так, используй команду /start, чтобы перезапустить бота. 🔁",
        parse_mode="Markdown"
    )
