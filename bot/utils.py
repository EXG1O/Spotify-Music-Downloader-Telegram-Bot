from aiogram.types import FSInputFile

from spotify import Song

from . import bot

from pathlib import Path
from typing import Any


async def reply_song(
    chat_id: int, user_message_id: int, song: Song, song_path: Path | None
) -> None:
    bot_message_kwargs: dict[str, Any] = {
        'chat_id': chat_id,
        'reply_to_message_id': user_message_id,
    }

    if song_path:
        await bot.send_audio(**bot_message_kwargs, audio=FSInputFile(song_path))
    else:
        await bot.send_message(
            **bot_message_kwargs,
            text=f'Failed to download <code>{song.display_name}</code>.',
        )
