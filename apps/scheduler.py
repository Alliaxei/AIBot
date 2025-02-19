from datetime import datetime

from aiogram import Bot
from sqlalchemy import select

from apps.database.database import async_session
from apps.database.models import User
from apps.database.requests import add_credits, moscow_tz

CREDITS_PER_DAY = 10

async def add_daily_credits(bot: Bot):
    async with async_session() as session:
        result = await session.execute(select(User.id))
        users = result.scalars().all()

        for user_id in users:
            await add_credits(session, user_id, CREDITS_PER_DAY)

        print(f"[{datetime.now(moscow_tz)}] Начислены кредиты {len(users)} пользователям.")