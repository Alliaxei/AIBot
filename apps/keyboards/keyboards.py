from aiogram.filters import callback_data
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiohttp import request
from openai.resources import AsyncUploads
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.database import requests
from apps.database.models import UserSettings

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🎨 Создание изображения', callback_data='generate_image')],
    [InlineKeyboardButton(text='👤 Личный кабинет', callback_data='profile'),
    InlineKeyboardButton(text='💳 Купить кредиты', callback_data='credits')],
    [InlineKeyboardButton(text='⚙️ Настройки', callback_data='settings'),
     InlineKeyboardButton(text='🖼️ Галерея', callback_data='gallery')]
])

credits = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='10 кредитов - 100р', callback_data='10credits'),
    InlineKeyboardButton(text='50 кредитов - 450р', callback_data='50credits')],
    [InlineKeyboardButton(text='100 кредитов - 850р', callback_data='100credits'),
    InlineKeyboardButton(text='250 кредитов - 2000р', callback_data='250credits')],
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='back')],
])

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Стиль изображений', callback_data='image_style')],
    [InlineKeyboardButton(text='Качество изображений', callback_data='image_quality')],
    [InlineKeyboardButton(text='Русский', callback_data='russian'),
     InlineKeyboardButton(text='English', callback_data='english')],
    [InlineKeyboardButton(text='⬅️ Вернуться в меню', callback_data='back')],
])

profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔄 Обновить данные', callback_data='update_data')],
    [InlineKeyboardButton(text='⬅️ Вернуться в меню', callback_data='back')],
])

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='back'),],
])
async def get_styles_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Создает клавиатуру с отметкой текущего выбранного стиля."""
    user = await requests.get_user(user_id)
    selected_style = user.settings.selected_style if user.settings else None
    _styles = [
        ("Schnell", "style_schnell"),
        ("Dev", "style_dev"),
        ("Inpainting", "style_inpainting"),
        ("Realism", "style_realism"),
        ("PRO", "style_pro"),
        ("PRO v1.1", "style_pro_v1_1"),
        ("Ultra", "style_ultra")
    ]

    def add_checkmark(name, _callback_data):
        return f'✅ {name}' if _callback_data == f'style_{selected_style}' else name

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=add_checkmark(name, cb_data), callback_data=cb_data)]
            for name, cb_data in _styles
        ]
    )

    keyboard.inline_keyboard.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_settings")])
    return keyboard

async def get_quality_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Создает клавиатуру с отметкой текущего выбранного разрешения."""
    user = await requests.get_user(user_id)
    selected_size = user.settings.image_size if user.settings else "512x512"
    _sizes = [
        ("512x512", "size_512x512"),
        ("1024x1024", "size_1024x1024"),
        ("2048x2048", "size_2048x2048")
    ]
    def add_checkmark(name, _callback_data):
        return f'✅ {name}' if _callback_data == f'size_{selected_size}' else name

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=add_checkmark(name, cb_data), callback_data=cb_data)]
            for name, cb_data in _sizes
        ]
    )
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_settings")])
    return keyboard

def get_next_page_keyboard(offset: int) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру с кнопкой "Далее" для подгрузки изображений.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⬅️ Назад', callback_data='back'),
        InlineKeyboardButton(text="▶️ Продолжить", callback_data=f"more_images_{offset}")]
    ])