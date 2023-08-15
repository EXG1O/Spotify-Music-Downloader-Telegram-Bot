from pathlib import Path
from dotenv import load_dotenv
import logging.config
import sqlite3
import os


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH: Path = BASE_DIR / 'DataBase.db'


load_dotenv()

API_TOKEN: str = os.getenv('API_TOKEN')

SPOTIFY_CLIENT_ID: str = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET: str = os.getenv('SPOTIFY_CLIENT_SECRET')


folders = ('logs', 'spotify_tracks')
for folder in folders:
	os.makedirs(BASE_DIR / folder, exist_ok=True)


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
