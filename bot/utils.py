from aiogram.types import FSInputFile, Message

from spotify import Song

from pathlib import Path


async def reply_song(message: Message, song: Song, path: Path | None) -> None:
    if path:
        await message.reply_audio(FSInputFile(path))
    else:
        await message.reply(f'Failed to download <code>{song.display_name}</code>.')
