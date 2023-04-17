from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

import scripts.decorators as Decorators

from threading import Thread
from fuzzywuzzy import fuzz
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

	@Decorators.get_attributes(need_attributes=('context', 'user_id', 'message_id', 'message',))
	def downloading_spotify_track(self, context: CallbackContext, user_id: int, message_id: int, message: str):
		context.bot.send_message(chat_id=user_id, text='Downloading Spotify track...')

		result = subprocess.check_output(['python', '-m', 'spotdl', message]).decode('UTF-8')
		if result.find('"') != -1:
			spotify_track_name = result.split('"')[1]
		else:
			spotify_track_name = result.split('Skipping ')[1].split(' (file already exists)')[0]

		for file_name in os.listdir('.'):
			if file_name.find('.mp3') != -1:
				if fuzz.partial_ratio(spotify_track_name, file_name) > 50:
					spotify_track_name = file_name.replace('.mp3', '')
					break

		with open(f'./{spotify_track_name}.mp3', 'rb') as spotify_track_file:
			spotify_track_file_bytes = spotify_track_file.read()
		os.remove(f'./{spotify_track_name}.mp3')

		context.bot.delete_message(chat_id=user_id, message_id=message_id+1)
		context.bot.send_audio(chat_id=user_id, audio=spotify_track_file_bytes, reply_to_message_id=message_id)

	@Decorators.get_attributes(need_attributes=('update', 'context', 'user_id', 'message',))
	def message_handler(self, update: Update, context: CallbackContext, user_id: int, message: str) -> None:
		if message.find('https://open.spotify.com/track/') != -1:
			th = Thread(target=self.downloading_spotify_track, args=(update, context), daemon=True)
			th.start()
		else:
			context.bot.send_message(chat_id=user_id, text='This is not a Spotify track link!')

	def start(self, spotify_music_downloader_telegram_bot_token: str) -> None:
		self.updater = Updater(token=spotify_music_downloader_telegram_bot_token)
		self.dispatcher = self.updater.dispatcher

		start_command_handler = CommandHandler('start', self.start_command)
		self.dispatcher.add_handler(start_command_handler)

		self.dispatcher.add_handler(MessageHandler(Filters.text, self.message_handler))

		self.updater.start_polling()
