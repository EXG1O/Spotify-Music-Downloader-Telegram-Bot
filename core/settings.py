from dotenv import load_dotenv

from pathlib import Path
from typing import Any, Final
import logging.config
import os

load_dotenv()


BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent

BOT_TOKEN: Final[str] = os.environ['BOT_TOKEN']

SPOTIFY_CLIENT_ID: Final[str] = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET: Final[str] = os.environ['SPOTIFY_CLIENT_SECRET']

POSTGRESQL_DATABASE_HOST: Final[str] = os.environ['POSTGRESQL_DATABASE_HOST']
POSTGRESQL_DATABASE_NAME: Final[str] = os.environ['POSTGRESQL_DATABASE_NAME']
POSTGRESQL_DATABASE_USER: Final[str] = os.environ['POSTGRESQL_DATABASE_USER']
POSTGRESQL_DATABASE_PASSWORD: Final[str] = os.environ['POSTGRESQL_DATABASE_PASSWORD']

DATABASE_URL: Final[str] = (
    f'postgresql+psycopg://{POSTGRESQL_DATABASE_USER}:{POSTGRESQL_DATABASE_PASSWORD}'
    f'@{POSTGRESQL_DATABASE_HOST}/{POSTGRESQL_DATABASE_NAME}'
)

MAX_SONGS_PER_DOWNLOAD_REQUEST: Final[int] = int(
    os.getenv('MAX_SONGS_PER_DOWNLOAD_REQUEST', '25')
)
MAX_PARALLEL_MUSIC_DOWNLOADS: Final[int] = int(
    os.getenv('MAX_PARALLEL_MUSIC_DOWNLOADS', '5')
)
MAX_TRACK_STORAGE_SIZE: Final[int] = int(
    os.getenv('MAX_TRACK_STORAGE_SIZE', '1073741824')
)

LOGS_PATH: Final[Path] = BASE_DIR / 'logs'
TRACKS_PATH: Final[Path] = BASE_DIR / 'tracks'

LOGGING: Final[dict[str, Any]] = {
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
            'level': 'INFO',
            'handlers': [
                'console',
                'info_file',
                'error_file',
            ],
            'propagate': True,
        },
    },
}

LOGS_PATH.mkdir(exist_ok=True)
TRACKS_PATH.mkdir(exist_ok=True)

logging.config.dictConfig(LOGGING)
