from datetime import datetime

from aiogram import Bot
from sqlalchemy import select

from apps.database.database import async_session
from apps.database.models import User
from apps.database.requests import add_credits, moscow_tz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

CREDITS_PER_DAY = 10
scheduler = AsyncIOScheduler()

async def daily_credits_scheduler():
    async with async_session() as session:
        users = await session.execute(select(User))
        users = users.scalars().all()

        for user in users:
            await add_credits(session, user.id, CREDITS_PER_DAY)

def start_scheduler():
    scheduler.add_job(daily_credits_scheduler, 'cron', hour=0, minute=0)
    scheduler.start()