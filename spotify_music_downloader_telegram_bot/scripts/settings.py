from pathlib import Path
import logging.config
import sqlite3
import json
import os


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / 'data/DataBase.db'


folders = ('data', 'logs', 'spotify_tracks',)
for folder in folders:
	if os.path.exists(BASE_DIR / folder) is False:
		os.mkdir(BASE_DIR / folder)


if os.path.exists(BASE_DIR / 'data/api.token') is False:
	open(BASE_DIR / 'data/api.token', 'w')

with open(BASE_DIR / 'data/api.token', 'r') as api_token_file:
	API_TOKEN = api_token_file.read().replace('\n', '')

if API_TOKEN == '':
	print(f"Enter the Spotify Music Downloader Telegram bot API-Token in the file {BASE_DIR / 'data/api.token'}!")

	exit()


if os.path.exists(BASE_DIR / 'data/spotify_settings.json') is False:
	with open(BASE_DIR / 'data/spotify_settings.json', 'w') as spotify_settings_file:
		json.dump(
			obj={
				'client_id': '',
				'client_secret': '',
			},
			fp=spotify_settings_file,
			indent=2
		)

with open(BASE_DIR / 'data/spotify_settings.json', 'r') as spotify_settings_file:
	SPOTIFY_SETTINGS = json.load(spotify_settings_file)

if SPOTIFY_SETTINGS['client_id'] == '' or SPOTIFY_SETTINGS['client_secret'] == '':
	print(f"Enter \"client_id\" and \"client_secret\" in the file {BASE_DIR / 'data/spotify_settings.json'}!")

	exit()


db = sqlite3.connect(DATABASE_DIR)
cursor = db.cursor()

cursor.execute("""
	CREATE TABLE IF NOT EXISTS User(
		id INTEGER NOT NULL PRIMARY KEY
	)
""")
db.commit()

db.close()


LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'standard': {
			'format': '[{asctime}]: {levelname} > {message}',
			'style': '{',
		},
	},
	'handlers': {
		'console': {
			'level': 'INFO',
			'class': 'logging.StreamHandler',
			'formatter': 'standard',
		},
		'info_file': { 
			'level': 'INFO',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': BASE_DIR / 'logs/info.log',
			'maxBytes': 10485760,
			'backupCount': 10,
			'formatter': 'standard',
		},
		'error_file': { 
			'level': 'ERROR',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': BASE_DIR / 'logs/error.log',
			'maxBytes': 10485760,
			'backupCount': 10,
			'formatter': 'standard',
		},
	},
	'loggers': {
		'root': {
			'handlers': [
				'console',
				'info_file',
				'error_file',
			],
			'propagate': True,
		},
	},
}

logging.config.dictConfig(LOGGING)
