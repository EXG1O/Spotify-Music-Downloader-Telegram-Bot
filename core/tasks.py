from aiogram.exceptions import TelegramAPIError

from sqlalchemy import select

from bot import bot
from bot.utils import reply_song
from database import async_session
from database.models import MusicDownloadQueue
from spotify import Song, spotify
from spotify.exceptions import TooManySongsPerDownloadRequestError

from .settings import (
    MAX_SONGS_PER_DOWNLOAD_REQUEST,
    MAX_TRACK_STORAGE_SIZE,
    TRACKS_PATH,
)

from collections.abc import Sequence
from contextlib import suppress
from pathlib import Path
from typing import Any
import asyncio
import os


async def check_downloaded_track_ages() -> None:
    while True:
        tracks: list[Path] = [
            TRACKS_PATH / track_path for track_path in os.listdir(TRACKS_PATH)
        ]
        total_size: int = sum(os.path.getsize(track) for track in tracks)

        if total_size > MAX_TRACK_STORAGE_SIZE:
            for track in sorted(tracks, key=lambda track: os.path.getatime(track)):
                track_size: int = os.path.getsize(track)

                os.remove(track)
                total_size -= track_size

                if total_size <= MAX_TRACK_STORAGE_SIZE:
                    break

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

        with suppress(TelegramAPIError):
            try:
                songs: list[tuple[Song, Path | None]] = await spotify.download(
                    request.query
                )

                if songs:
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
                else:
                    await bot.edit_message_text(
                        **bot_message_kwargs,
                        text=(
                            "I couldn't download anything from this link."
                            'Please try another one'
                        ),
                    )
            except TooManySongsPerDownloadRequestError:
                await bot.edit_message_text(
                    **bot_message_kwargs,
                    text=(
                        f'We found more than {MAX_SONGS_PER_DOWNLOAD_REQUEST} songs at your link, '
                        'which exceeds the limit for adding songs to the download queue.'
                    ),
                )

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
