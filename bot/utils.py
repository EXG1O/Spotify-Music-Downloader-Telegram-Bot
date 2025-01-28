from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import Chat, FSInputFile, Message

from spotdl import Song

from spotify import spotify

from pathlib import Path
import asyncio


async def download_and_send_song(
    bot: Bot, chat: Chat, message: Message, song: Song
) -> None:
    try:
        download_song: tuple[Song, Path] = await spotify.download(song=song)
        await message.reply_audio(audio=FSInputFile(path=download_song[1]))
    except TelegramRetryAfter as error:
        await asyncio.sleep(error.retry_after)
        return await download_and_send_song(bot, chat, message, song)
