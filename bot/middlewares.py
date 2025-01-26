from aiogram import BaseMiddleware
from aiogram.types import Update
from aiogram.types import User as TUser

from sqlalchemy import select

from database import async_session
from database.models import User

from collections.abc import Awaitable, Callable
from typing import Any

Handler = Callable[[Update, dict[str, Any]], Awaitable[Any]]


class CreateUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Handler,
        event: Update,  # type: ignore [override]
        data: dict[str, Any],
    ) -> Any:
        event_from_user: TUser = data['event_from_user']
        user_telegram_id: int = event_from_user.id

        async with async_session() as session:
            user: User | None = await session.scalar(
                select(User).where(User.telegram_id == user_telegram_id)
            )
            is_new_user: bool = not user

            if is_new_user:
                user = User(telegram_id=user_telegram_id)

                session.add(user)
                await session.commit()
                await session.refresh(user)

        data['user'] = user
        data['is_new_user'] = is_new_user

        return await handler(event, data)
