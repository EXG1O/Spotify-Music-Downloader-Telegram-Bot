from aiogram.exceptions import TelegramAPIError

from sqlalchemy import select

from bot import bot
from bot.utils import reply_song
from database import async_session
from database.models import MusicDownloadQueue
from spotify import Song, spotify

from .settings import TRACKS_PATH

from collections.abc import Sequence
from contextlib import suppress
from pathlib import Path
from typing import Any
import asyncio
import os
import time


async def check_downloaded_track_ages() -> None:
    while True:
        for track in os.listdir(TRACKS_PATH):
            track_path: Path = TRACKS_PATH / track
            track_age: float = time.time() - os.path.getatime(track_path)

            if track_age > 604800:
                os.remove(track_path)

        await asyncio.sleep(3600)


async def process_music_download_request(request_id: int) -> None:
    async with async_session() as session:
        request: MusicDownloadQueue | None = await session.scalar(
            select(MusicDownloadQueue).where(MusicDownloadQueue.id == request_id)
        )

        if not request:
            return

        chat_id: int = request.chat_id
        bot_message_id: int = request.bot_message_id
        user_message_id: int = request.user_message_id

        bot_message_kwargs: dict[str, Any] = {
            'chat_id': chat_id,
            'message_id': bot_message_id,
        }

        songs: list[tuple[Song, Path | None]] = await spotify.download(request.query)

        with suppress(TelegramAPIError):
            if not songs:
                await bot.edit_message_text(
                    **bot_message_kwargs,
                    text=(
                        "I couldn't download anything from this link."
                        'Please try another one'
                    ),
                )
                return

            await asyncio.gather(
                *[
                    reply_song(
                        chat_id=chat_id,
                        user_message_id=user_message_id,
                        song=song,
                        song_path=path,
                    )
                    for song, path in songs
                ]
            )
            await bot.delete_message(**bot_message_kwargs)

        await session.delete(request)
        await session.commit()


async def process_music_download_queue() -> None:
    while True:
        async with async_session() as session:
            request_ids: Sequence[int] = (
                await session.scalars(select(MusicDownloadQueue.id))
            ).all()

        await asyncio.gather(
            *[process_music_download_request(request_id) for request_id in request_ids],
            return_exceptions=True,
        )
        await asyncio.sleep(1)


async def run_tasks() -> None:
    asyncio.create_task(check_downloaded_track_ages())
    asyncio.create_task(process_music_download_queue())
