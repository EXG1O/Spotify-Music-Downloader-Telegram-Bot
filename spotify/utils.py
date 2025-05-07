from spotdl import Spotdl
from spotdl.types.options import DownloaderOptions
from spotdl.utils.spotify import SpotifyClient

from core.settings import TRACKS_PATH

from collections.abc import Generator
from contextlib import contextmanager
from typing import Final
import os

SPOTDL_DOWNLOADER_SETTINGS: Final[DownloaderOptions] = {
    'threads': max(1, (os.cpu_count() or 2) // 2),
    'bitrate': '256k',
    'output': str(TRACKS_PATH),
    'simple_tui': True,
}


@contextmanager
def spotdl_client(client_id: str, client_secret: str) -> Generator[Spotdl, None, None]:
    SpotifyClient._instance = None
    yield Spotdl(
        client_id, client_secret, downloader_settings=SPOTDL_DOWNLOADER_SETTINGS
    )
