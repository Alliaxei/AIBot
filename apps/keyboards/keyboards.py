from aiogram.filters import callback_data
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📹 Создание видео', callback_data='generate_video')],
    [InlineKeyboardButton(text='🔍 Запрос к DeepSeek', callback_data='deepseek'),
     InlineKeyboardButton(text='📊 Личный кабинет', callback_data='profile')],
    [InlineKeyboardButton(text='💳 Купить кредиты', callback_data='credits'),
     InlineKeyboardButton(text='ℹ️ О нас', callback_data='about_site')],
])

profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔄 Обновить данные', callback_data='update_data')],
    [InlineKeyboardButton(text='⬅️ Вернуться в меню', callback_data='back')],
])
back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Назад', callback_data='back'),],
])

