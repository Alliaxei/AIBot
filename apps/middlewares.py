from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from apps.database.database import async_session

class DbSessionMiddleware(BaseMiddleware):
    async def on_process_message(self, message, data):
        # Создание новой сессии и добавление её в контекст данных
        data['session'] = async_session()

    async def on_post_process_message(self, message, data):
        """Закрываем сессию после обработки сообщения."""
        session: AsyncSession = data.get('session')
        if session:
            await session.close()
