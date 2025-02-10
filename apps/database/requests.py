from apps.database.database import async_session
from apps.database.models import User
from sqlalchemy import select

async def set_user(tg_id, username: str = None, first_name: str = None) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == tg_id))

        if not user:
            new_user = User(
                telegram_id=tg_id,
                username=username,
                first_name=first_name,
                credits_left=10,
            )

            session.add(new_user)
            await session.commit()

async def update_user(tg_id: int, username: str = None, first_name: str = None) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == tg_id))
        if not user:
            raise ValueError(f"Пользователь с telegram_id {tg_id} не найден")

        if username is not None:
            user.username = username
        if first_name is not None:
            user.first_name = first_name

        await session.commit()

async def get_user(telegram_id: int) -> User | None:
    async with async_session() as session:
        return await session.scalar(select(User).where(User.telegram_id == telegram_id))