from aiogram import Bot
from aiogram.enums import ChatAction
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
        await bot.send_chat_action(chat_id=chat.id, action=ChatAction.UPLOAD_VOICE)

        download_song: tuple[Song, Path] = await spotify.download(song=song)

        await bot.send_chat_action(chat_id=chat.id, action=ChatAction.UPLOAD_VOICE)
        await message.reply_audio(audio=FSInputFile(path=download_song[1]))
    except TelegramRetryAfter as error:
        await asyncio.sleep(error.retry_after)
        return await download_and_send_song(bot, chat, message, song)
