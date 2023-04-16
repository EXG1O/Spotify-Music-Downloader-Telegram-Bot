from scripts.telegram_bot import SpotifyMusicDownloaderTelegramBot
import scripts.functions as Functions

import logging
import os

def main() -> None:
	if Functions.if_find_folder_or_file('./data', 'spotify_music_downloader_telegram_bot.token'):
		with open('./data/spotify_music_downloader_telegram_bot.token', 'r') as spotify_music_downloader_telegram_bot_token_file:
			spotify_music_downloader_telegram_bot_token = spotify_music_downloader_telegram_bot_token_file.read()
	else:
		open('./data/spotify_music_downloader_telegram_bot.token', 'w')
		spotify_music_downloader_telegram_bot_token = ''

	if spotify_music_downloader_telegram_bot_token == '':
		print('Enter the Constructor Telegram bot token in the file ./data/spotify_music_downloader_telegram_bot.token!')
	else:
		spotify_music_downloader_telegram_bot = SpotifyMusicDownloaderTelegramBot()
		spotify_music_downloader_telegram_bot.start(spotify_music_downloader_telegram_bot_token)

if __name__ == '__main__':
	if Functions.if_find_folder_or_file('.', 'data') is False:
		os.mkdir('./data')

	logging.basicConfig(filename='./data/spotify_music_downloader_telegram_bot.log', filemode='a', format='[%(asctime)s]: %(levelname)s > %(message)s', level=logging.INFO)

	main()
