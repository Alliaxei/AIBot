from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apps.database import requests


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🎨 Создать изображение', callback_data='generate_image')],
    [InlineKeyboardButton(text='👤 Личный кабинет', callback_data='profile'),
    InlineKeyboardButton(text='💳 Купить кредиты', callback_data='credits')],
    [InlineKeyboardButton(text='⚙️ Настройки', callback_data='settings'),
     InlineKeyboardButton(text='🖼️ Галерея', callback_data='gallery')]
])

generate_new_image = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🎨 Создать ещё одно изображение', callback_data='generate_image')],
    [InlineKeyboardButton(text='⬅️ Вернуться на главную', callback_data='back')],
])

credits = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='50 кредитов - 450₽', callback_data='credits_50:450'),
    InlineKeyboardButton(text='200 кредитов - 1800₽', callback_data='credits_200:1800')],
    [InlineKeyboardButton(text='500 кредитов - 4500₽', callback_data='credits_500:4500'),
    InlineKeyboardButton(text='1000 кредитов - 8500₽', callback_data='credits_1000:8500')],
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='back')],
])

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Стиль изображений', callback_data='image_style')],
    [InlineKeyboardButton(text='Качество изображений', callback_data='image_quality')],
    [InlineKeyboardButton(text='⬅️ Вернуться в меню', callback_data='back')],
])

profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔄 Обновить данные', callback_data='update_data')],
    [InlineKeyboardButton(text='⬅️ Вернуться в меню', callback_data='back')],
])

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='back')],
])

def add_checkmark_to_button(name, _callback_data, selected_value):
    """Добавляет галочку к кнопке, если она выбрана."""
    return f'✅ {name}' if _callback_data == selected_value else name

async def get_styles_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Создает клавиатуру с отметкой текущего выбранного стиля."""
    user = await requests.get_user(user_id)
    selected_style = user.settings.selected_style if user.settings else None
    _styles = [
        ("Schnell", "style_schnell"),
        ("Dev", "style_dev"),
        ("Realism", "style_realism"),
        ("PRO", "style_pro"),
        ("Ultra", "style_ultra"),
        ("Inpainting", "style_inpainting"),
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=add_checkmark_to_button(name, cb_data, f'style_{selected_style}'),
                                  callback_data=cb_data)]
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
        ("1536x1536", "size_1536x1536")
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=add_checkmark_to_button(name, cb_data, f'size_{selected_size}'),
                                  callback_data=cb_data)]
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

def get_payment_keyboard(url: str, order_id: int, amount: int) -> InlineKeyboardMarkup:
    payment = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💳 Оплатить', url=url)],
        [InlineKeyboardButton(text='🔄 Проверить', callback_data=f"check_payment:{order_id}_{amount}")],
        [InlineKeyboardButton(text='⬅️ Назад', callback_data='back_to_payment')],
    ])
    return payment