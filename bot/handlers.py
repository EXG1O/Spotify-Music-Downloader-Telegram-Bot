from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Chat, Message, User

from core.settings import BOT_TOKEN
from database import async_session
from database.models import MusicDownloadQueue

from .middlewares import CreateUserMiddleware
from .session import ResilientSession

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
            f'<b>Hi, {event_from_user.full_name}!</b>\n\n'
            'I\'m a free <a href="https://github.com/EXG1O/Spotify-Music-Downloader-Telegram-Bot">open-source</a> Telegram bot '
            'that helps you download music from Spotify — just send me a link.\n\n'
            'If you want to support the developer, you can make a donation using one of '
            'the methods mentioned in this <a href="https://t.me/exg1o_channel/107">post</a>.\n\n'
            "You can also subscribe to the @exg1o_channel, the developer's Telegram channel, "
            'to stay updated on news and other projects.\n\n'
            '<b>Note:</b> playlist downloads may not always work perfectly.'
        ),
    )


@dispatcher.message()
async def message_handler(message: Message, event_chat: Chat) -> None:
    query: str | None = message.text

    if not query:
        return None

    bot_message: Message = await message.reply(
        'Downloading music... This might may take a few minutes.'
    )

    async with async_session() as session:
        session.add(
            MusicDownloadQueue(
                chat_id=event_chat.id,
                bot_message_id=bot_message.message_id,
                user_message_id=message.message_id,
                query=query,
            )
        )
        await session.commit()
