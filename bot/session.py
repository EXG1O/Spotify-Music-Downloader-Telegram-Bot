from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.exceptions import TelegramRetryAfter
from aiogram.methods.base import TelegramMethod, TelegramType

import asyncio


class ResilientSession(AiohttpSession):
    async def make_request(
        self, bot: Bot, method: TelegramMethod[TelegramType], timeout: int | None = None
    ) -> TelegramType:
        try:
            return await super().make_request(bot, method, timeout)
        except TelegramRetryAfter as error:
            await asyncio.sleep(error.retry_after)
            return await self.make_request(bot, method, timeout)
