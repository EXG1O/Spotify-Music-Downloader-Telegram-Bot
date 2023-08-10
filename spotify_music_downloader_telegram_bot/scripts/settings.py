from pathlib import Path
import logging.config
import sqlite3
import json
import os


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH: Path = BASE_DIR / 'data/DataBase.db'


folders = ('data', 'logs', 'spotify_tracks')
for folder in folders:
	os.makedirs(BASE_DIR / folder, exist_ok=True)


api_token_path: Path = BASE_DIR / 'data/api.token'

if not os.path.exists(api_token_path):
	open(api_token_path, 'w')

with open(api_token_path, 'r') as api_token_file:
	API_TOKEN: str = api_token_file.read().replace('\n', '')

if not API_TOKEN:
	print(f"Enter the Spotify Music Downloader Telegram bot API-Token in the file {api_token_path}!")
	exit()


spotify_settings_path: Path = BASE_DIR / 'data/spotify_settings.json'

if not os.path.exists(spotify_settings_path):
	with open(spotify_settings_path, 'w') as spotify_settings_file:
		json.dump({
			'client_id': '',
			'client_secret': '',
		}, spotify_settings_file, indent=2)

with open(spotify_settings_path, 'r') as spotify_settings_file:
	SPOTIFY_SETTINGS: dict = json.load(spotify_settings_file)

if not SPOTIFY_SETTINGS['client_id'] or not SPOTIFY_SETTINGS['client_secret']:
	print(f"Enter \"client_id\" and \"client_secret\" in the file {spotify_settings_path}!")
	exit()


db = sqlite3.connect(DATABASE_PATH)
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
