from aiogram import Router, F

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from apps.keyboards import keyboards as kb
from apps.database import requests
from apps.states import DeepSeekState, VideoState

router = Router()

def get_profile_text(user) -> str:
    return (
        "✨ *Добро пожаловать в Личный кабинет* ✨\n\n"
        f"👤 Имя: *{user.first_name or 'Не указано'}*\n"
        f"🌐 Username: *@{user.username or 'Не указано'}*\n"
        f"📌 Telegram ID: `{user.telegram_id}`\n\n"
        f"💰 Кредиты: *{user.credits_left or 'Не указано'}* шт.\n\n"
        "=======================\n"
        "Выберите действие:\n"
    )

@router.callback_query(F.data == 'profile')
async def profile_handler(callback: CallbackQuery):
    user = await requests.get_user(callback.from_user.id)

    if user is None:
        await callback.message.edit_text(
            text='Ошибка, пользователь не найден\nПопробуйте перезапустить бота с помощью команды /start',
            reply_markup=kb.back
        )
        return
    profile_text = get_profile_text(user)

    await callback.message.edit_text(
        text=profile_text,
        parse_mode="Markdown",
        reply_markup=kb.profile
    )

@router.callback_query(F.data == 'update_data')
async def update_data_handler(callback: CallbackQuery):
    user = await requests.get_user(callback.from_user.id)
    if user is None:
        await callback.answer("❌ Пользователь не найден. Попробуйте перезапустить бота с помощью команды /start.")
        return

    try:
        await requests.update_user(
            tg_id=callback.from_user.id,
            username=callback.from_user.username,
            first_name=callback.from_user.first_name,
        )
        updated_user = await requests.get_user(callback.from_user.id)
        if updated_user is None:
            await callback.answer("❌ Не удалось получить обновленные данные.")
            return

        profile_text = get_profile_text(updated_user)
        await callback.message.edit_text(
            text=profile_text,
            parse_mode="Markdown",
            reply_markup=kb.profile
        )
        await callback.answer("✅ Ваши данные успешно обновлены.")
    except Exception as e:
        await callback.answer(f"❌ Не удалось обновить данные: {str(e)}")

@router.callback_query(F.data == 'deepseek')
async def deepseek_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите ваш запрос ...', reply_markup=kb.back)
    await state.set_state(DeepSeekState.waiting_for_promt)

@router.callback_query(F.data == 'generate_video')
async def generate_video_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите текстовое описание видео', reply_markup=kb.back)
    await state.set_state(VideoState.waiting_for_promt)

@router.callback_query(F.data == 'back')
async def back_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Вы на главной странице', reply_markup=kb.main)
    await state.clear()