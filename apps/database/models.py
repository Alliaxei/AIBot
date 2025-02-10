from datetime import datetime

from sqlalchemy import BIGINT, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from apps.database.database import Base, engine
from sqlalchemy import String
from sqlalchemy import func

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id = mapped_column(BIGINT)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    username: Mapped[str] = mapped_column(String(50), nullable=True)
    credits_left: Mapped[int] = mapped_column(Integer, nullable=True)

class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    amount: Mapped[int] = mapped_column()
    transaction_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
