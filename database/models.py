from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(BIGINT(), primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BIGINT(), unique=True, index=True)
