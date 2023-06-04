from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, InputFile
from aiogram import Bot

from scripts.settings import API_TOKEN, BASE_DIR, SPOTIFY_SETTINGS

from spotdl import Spotdl, DownloaderOptions
import asyncio
import logging
import time
import os


logger = logging.getLogger('root')
logger.setLevel(logging.NOTSET)


loop = asyncio.get_event_loop()

bot = Bot(token=API_TOKEN, loop=loop)
dispatcher = Dispatcher(bot=bot)

spotdl = Spotdl(
	**SPOTIFY_SETTINGS,
	downloader_settings=DownloaderOptions(output='spotify_tracks')
)


@dispatcher.message_handler(commands=['start'])
async def send_welcome(message: Message) -> None:
	logger.info(f'{message.from_user.url}: {message.text}')

	if message.from_user.language_code == 'ru':
		message_text = f"""\
			Привет, @{message.from_user.username}!
			Я являюсь Telegram ботом для скачивания музыки с Spotify.
			Отправьте мне ссылку на Spotify трек, и я отправлю тебе этот трек.
		"""
	else:
		message_text = f"""\
			Hello, @{message.from_user.username}!
			I am a Telegram Bot for downloading music from Spotify.
			Send me the link to the Spotify track and I will send that track to you.
		"""

	sent_message = await bot.send_message(chat_id=message.chat.id, text=message_text.replace('	', ''))
	logger.info(f'Spotify Music Downloader Telegram Bot: {sent_message.text}')

@dispatcher.message_handler()
async def send_spotify_track(message: Message) -> None:
	logger.info(f'{message.from_user.url}: {message.text}')
	if message.text.find('https://open.spotify.com/track/') != -1:
		if message.from_user.language_code == 'ru':
			message_text = 'Скачиваю Spotify трек...'
		else:
			message_text = 'Downloading Spotify track...'

		sent_message = await bot.send_message(chat_id=message.chat.id, text=message_text)
		logger.info(f'Spotify Music Downloader Telegram Bot: {sent_message.text}')

		spotify_track = spotdl.search(query=[message.text])[0]
		spotify_track, path_to_spotify_track = spotdl.downloader.search_and_download(song=spotify_track)
		path_to_spotify_track = BASE_DIR / path_to_spotify_track

		await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
		
		await message.reply_audio(audio=InputFile(path_to_spotify_track))
		logger.info(f'Spotify Music Downloader Telegram Bot: Sent Spotify track "{spotify_track.display_name}".')
	else:
		if message.from_user.language_code == 'ru':
			message_text = 'Это не ссылка на Spotify трек!'
		else:
			message_text = 'This is not a Spotify track link!'
		
		sent_message = await message.reply(text=message_text)
		logger.info(f'Spotify Music Downloader Telegram Bot: {sent_message.text}')

async def check_downloaded_spotify_tracks() -> None:
	while True:
		for spotify_track in os.listdir(BASE_DIR / 'spotify_tracks'):
			spotify_track_path = BASE_DIR / 'spotify_tracks' / spotify_track
			
			spotify_track_age = time.time() - os.path.getatime(spotify_track_path)
			if spotify_track_age > 7 * 24 * 60 * 60:
				logger.info(f'Removed Spotify track "{spotify_track}" age={spotify_track_age / 60 / 60 / 24} hours.')
				os.remove(spotify_track_path)
		
		await asyncio.sleep(60 * 60)

async def start() -> None:
	logger.info('Start asynchronous function for check downloaded spotify tracks.')
	
	asyncio.create_task(check_downloaded_spotify_tracks())

	logger.info('Starting Spotify Music Downloader Telegram Bot.')
	
	count = await dispatcher.skip_updates()

	logger.info(f'Skipped {count} updates.')

	await dispatcher.start_polling()


if __name__ == '__main__':
	try:
		loop.run_until_complete(start())
	except KeyboardInterrupt:
		loop.stop()
