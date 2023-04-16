from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.callbackcontext import CallbackContext

import scripts.decorators as Decorators

import subprocess
import os

class SpotifyMusicDownloaderTelegramBot:
	@Decorators.get_attributes(need_attributes=('context', 'user_id', 'username',))
	def start_command(self, context: CallbackContext, user_id: int, username: str) -> None:
		context.bot.send_message(
			chat_id=user_id,
			text=f"""\
				Hello, @{username}!
				I am a Telegram Bot for downloading music from Spotify.
				Send me a Spotify link to a track and I'll send that track.
			""".replace('	', '')
		)

	@Decorators.get_attributes(need_attributes=('context', 'user_id', 'message',))
	def message_handler(self, context: CallbackContext, user_id: int, message: str) -> None:
		if message.find('https://open.spotify.com/track/') != -1:
			context.bot.send_message(chat_id=user_id, text='Downloading Spotify track...')

			subprocess.check_output(['spotdl', message]).decode('UTF-8')

			for _file in os.listdir('.'):
				if _file.find('.mp3') != -1:
					with open(f'./{_file}', 'rb') as __file:
						audio = __file.read()
						context.bot.send_audio(chat_id=user_id, audio=audio)

						os.remove(f'./{_file}')

					break
		else:
			context.bot.send_message(chat_id=user_id, text='This is not a Spotify link!')

	def start(self, spotify_music_downloader_telegram_bot_token: str) -> None:
		self.updater = Updater(token=spotify_music_downloader_telegram_bot_token)
		self.dispatcher = self.updater.dispatcher

		start_command_handler = CommandHandler('start', self.start_command)
		self.dispatcher.add_handler(start_command_handler)

		self.dispatcher.add_handler(MessageHandler(Filters.text, self.message_handler))

		self.updater.start_polling()
