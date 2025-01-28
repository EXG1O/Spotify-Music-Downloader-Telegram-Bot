from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import Chat, FSInputFile, Message

from spotdl import Song

from spotify import spotify

import asyncio


async def download_and_send_song(
    bot: Bot, chat: Chat, message: Message, song: Song
) -> None:
    try:
        song, path = await spotify.download(song)

        if not path:
            await message.reply(
                text=(
                    f'Failed to download the song «{song.display_name}», '
                    'please try again later.'
                )
            )
            return

        await message.reply_audio(FSInputFile(path))
    except TelegramRetryAfter as error:
        await asyncio.sleep(error.retry_after)
        return await download_and_send_song(bot, chat, message, song)
