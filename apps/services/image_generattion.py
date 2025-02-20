import os

import aiohttp
from dotenv import load_dotenv

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.database.models import User
from apps.database.requests import get_current_credit_balance, get_session, spend_credits
from apps.database.models import Gallery

MEDIA_PATH = 'media/images'
load_dotenv('.env')
os.makedirs(MEDIA_PATH, exist_ok=True)

API_URL = 'https://api.gen-api.ru/api/v1/networks/flux'

MODEL_COSTS = {
    "schnell": 0.5,
    "dev": 4.5,
    "realism": 6.5,
    "pro": 9,
    "ultra": 13,
    "inpainting": 13.5,
}

SIZE_COSTS = {
    "512x512": 1,
    "1024x1024": 2,
    "1536x1536": 3,
}

async def get_user_db_id(session: AsyncSession, user_id: int) -> int | None:
    user = await session.execute(
        select(User.id).where(User.telegram_id == user_id)
    )
    return  user.scalar()


async def save_image_do_db(session: AsyncSession, user_id: int, image_url: str) -> None:
    user_id_db: int = await get_user_db_id(session, user_id)

    if user_id_db is None:
        return

    new_image = Gallery(user_id=user_id_db, image_url=image_url)
    session.add(new_image)
    await session.commit()

async def calculate_total_price(model_ration: float, size_ratio: float) -> float | None:
    """ Высчитывает итоговый ценник по формуле """
    k_1 = 20
    fixed_ratio = 5

    total_cost = model_ration * k_1 * size_ratio + fixed_ratio
    return total_cost

async def generate_image(prompt: str, model: str, size: str, user_id: int) -> str | None:
    """
    Отправляет запрос к API генерации изображений.
    Возвращает путь к загруженному изображению или None в случае ошибки.
    """

    # model_cost = MODEL_COSTS.get(model, 0)
    # size_cost = SIZE_COSTS.get(size, 0)
    #
    # if model_cost == 0:
    #     print(f"Ошибка: модель {model} не найдена в MODEL_COSTS.")
    #     return None
    # if size_cost == 0:
    #     print(f"Ошибка: размер {size} не найден в SIZE_COSTS.")
    #     return None
    #
    # total_cost = await calculate_total_price(model_cost, size_cost)
    #
    # session = await get_session()
    # async with session:
    #     current_balance = await get_current_credit_balance(session, user_id)
    #     if current_balance is None or current_balance < total_cost:
    #         print(f"Недостаточно кредитов у пользователя {user_id}. Текущий баланс: {current_balance}")
    #         return None
    #
    #     if not await spend_credits(session, user_id, total_cost):
    #         print(f"Ошибка списания кредитов у пользователя {user_id}")
    #         return None
    #
    # width, height = size.split('x')
    #
    # headers = {
    #     "Authorization": f"Bearer {os.getenv('GEN_API_KEY')}",
    #     "Content-Type": "application/json",
    #     "Accept": "application/json"
    # }
    #
    # payload = {
    #     "prompt": prompt,
    #     "model": model,
    #     "width": width,
    #     "height": height,
    #     "is_sync": True,
    # }
    #
    # try:
    #     async with aiohttp.ClientSession() as session:
    #         async with session.post(API_URL, json=payload, headers=headers) as response:
    #             print(f"Ответ от API: {response.status}")
    #
    #             content_type = response.headers.get('Content-Type', '')
    #
    #             if response.status == 200 and content_type.startswith('application/json'):
    #                 data = await response.json()
    #                 print(f"Ответ от API: {data}")
    #
    #                 image_list = data.get('images', [])
    #                 if not image_list:
    #                     print("Не удалось извлечь URL изображения из ответа.")
    #                     return None
    #
    #                 image_url = image_list[0]
    #                 print(f"URL изображения получен: {image_url}")
    #
    #                 async with await get_session() as db_session:
    #                     await save_image_do_db(db_session, user_id, image_url)
    #
    #                 return image_url
    #             else:
    #                 error_text = await response.text()
    #                 print(f"Ошибка {response.status}, ответ от API:\n{error_text}")
    # except Exception as e:
    #     print(f"Ошибка при генерации изображения: {e}")
    #
    # return None

    return 'https://gen-api.storage.yandexcloud.net/input_files/1739787209_67b30bc98f057.png'

