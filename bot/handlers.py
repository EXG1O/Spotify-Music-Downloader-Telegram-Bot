from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Chat, FSInputFile, Message, User

from core.settings import BOT_TOKEN
from spotify import spotify

from .middlewares import CreateUserMiddleware
from .session import ResilientSession

from pathlib import Path

bot = Bot(
    token=BOT_TOKEN,
    session=ResilientSession(),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML, link_preview_is_disabled=True
    ),
)

dispatcher = Dispatcher(bot=bot)
dispatcher.update.middleware(CreateUserMiddleware())


@dispatcher.message(CommandStart())
async def start_command_handler(message: Message, event_from_user: User) -> None:
    await message.answer(
        (
            f'Hello, {event_from_user.full_name}!\n\n'
            'I\'m a free <a href="https://github.com/EXG1O/Spotify-Music-Downloader-Telegram-Bot">open-source</a> '
            'Telegram bot for downloading music from Spotify using your link.\n\n'
            'Send me a Spotify link, and I will download its content and send it to you.\n\n'
            'If you like how I work and want to support the developer, '
            'you can make a donation using one of the methods mentioned in this <a href="https://t.me/exg1o_channel/107">post</a>.\n\n'
            "You can also subscribe to the @exg1o_channel, the developer's Telegram channel, to stay updated on news and other projects.\n\n"
            '<b>Note:</b> downloading music from a Spotify playlist may not always work correctly.'
        ),
    )


@dispatcher.message()
async def message_handler(message: Message, event_chat: Chat) -> None:
    if not message.text:
        return None

    bot_message: Message = await message.reply(
        'Downloading music from the link...\nThis process may take a few minutes.'
    )

    songs: list[Path] | None = await spotify.download(message.text)

    if not songs:
        await bot_message.edit_text(
            'Could not find or download music at the link, please try again later or send a different link.'
        )
        return

    for song in songs:
        await message.reply_audio(FSInputFile(song))
    await bot_message.delete()
