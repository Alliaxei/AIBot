from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.context import FSMContext
from apps.keyboards import keyboards as kb
from apps.database import requests
from apps.handlers.callbacks import show_profile
from apps.states import ImageState, BuyingState
router = Router()

@router.message(Command('start'))
async def start_handler(message: Message):
    await requests.set_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    await message.answer("🌟 Привет! Рад тебя видеть в Flux AI! 🎉\nНаш бот поможет тебе создавать потрясающие изображения. Выбирай, что хочешь, и давай начнем! 👇😊",
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

@router.message(Command('profile'))
async def profile_handler(message: Message):
    await show_profile(message)

@router.message(Command('generate'))
async def generate_handler(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer('Введите запрос в формате `/generate ваш запрос`', parse_mode="Markdown")
        return
    user_request = args[1]
    await message.answer(f"✅ Генерирую изображение по запросу: `{user_request}`\nОжидайте...", parse_mode="Markdown")

@router.message(Command('buy'))
async def buy_handler(message: Message, state: FSMContext):
    await message.answer('Выберите сумму для пополнения (больше - дешевле)', reply_markup=kb.credits)
    await state.set_state(BuyingState.waiting_for_transaction)

@router.message(Command('settings'))
async def settings_handler(message: Message):
    await message.answer(text='⚙️ Конфигурация и настройки ⚙️', reply_markup=kb.settings)

@router.message(Command('styles'))
async def styles_handler(message: Message):
    user = await requests.get_user(message.from_user.id)

    if not user:
        await message.answer("❌ Ошибка: пользователь не найден.")
        return

    keyboard = await kb.get_styles_keyboard(user.telegram_id)
    await message.answer("🎨 Выберите стиль изображения:", reply_markup=keyboard)

@router.message(Command('quality'))
async def size_handler(message: Message):
    user = await requests.get_user(message.from_user.id)
    if not user:
        await message.answer("❌ Ошибка: пользователь не найден.")
        return
    keyboard = await kb.get_quality_keyboard(user.telegram_id)
    await message.answer("🎨 Выберите размер изображения:", reply_markup=keyboard)