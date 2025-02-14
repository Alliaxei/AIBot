from sqlalchemy.orm import joinedload

from apps.database.database import async_session
from apps.database.models import User, UserSettings
from sqlalchemy import select

async def set_user(tg_id, username: str = None, first_name: str = None) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == tg_id))

        if not user:
            new_user = User(
                telegram_id=tg_id,
                username=username,
                first_name=first_name,
                credits=10,
            )
            session.add(new_user)
            await session.flush()

            new_settings = UserSettings(user_id=new_user.id)
            session.add(new_settings)

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
        return await session.scalar(
            select(User).options(joinedload(User.settings)).where(User.telegram_id == telegram_id)
        )

#Вынести в отдельную функцию
async def get_or_create_user_settings(session, tg_id: int, field: str, value: str):
    """Получает настройки пользователя или создает новые."""
    user = await session.scalar(select(User).where(User.telegram_id == tg_id))
    if not user:
        raise ValueError(f'Пользователь с telegram_id {tg_id} - не найден')

    settings = await session.scalar(select(UserSettings).where(UserSettings.user_id == user.id))
    if not settings:
        settings = UserSettings(user_id=user.id, **{field: value})
        session.add(settings)
    else:
        setattr(settings, field, value)

    return settings


async def update_user_style(tg_id: int, new_style: str = None) -> None:
    async with async_session() as session:
        await get_or_create_user_settings(session, tg_id, 'selected_style', new_style)
        await session.commit()


async def update_user_size(tg_id: int, new_size: str = None) -> None:
    async with async_session() as session:
        await get_or_create_user_settings(session, tg_id, 'image_size', new_size)
        await session.commit()
