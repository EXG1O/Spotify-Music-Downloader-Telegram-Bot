from spotdl import Spotdl
from spotdl.types.options import DownloaderOptions
from spotdl.types.song import Song

from core.settings import MAX_PARALLEL_MUSIC_DOWNLOADS, TRACKS_PATH

from asyncio import Semaphore
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from pathlib import Path
from typing import Final
import asyncio

spotify_download_semaphore = Semaphore(MAX_PARALLEL_MUSIC_DOWNLOADS)

SPOTDL_DOWNLOADER_SETTINGS: Final[DownloaderOptions] = {
    'threads': 1,
    'bitrate': '256k',
    'output': str(TRACKS_PATH),
    'simple_tui': True,
}


def _run_spotdl(
    connection: Connection, client_id: str, client_secret: str, query: str
) -> None:
    "DON'T CALL THIS FUNCTION FROM THE MAIN PROCESS BECAUSE `SpotDL` HAS A MEMORY LEAK."
    try:
        spotdl = Spotdl(
            client_id, client_secret, downloader_settings=SPOTDL_DOWNLOADER_SETTINGS
        )
        songs: list[Song] = spotdl.search([query])
        connection.send(spotdl.download_songs(songs))
    except Exception:
        connection.send([])


class Spotify:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

    def _download(self, query: str) -> list[tuple[Song, Path | None]]:
        parent_connection, child_connection = Pipe()

        process = Process(
            target=_run_spotdl,
            args=(child_connection, self.client_id, self.client_secret, query),
        )
        process.start()

        return parent_connection.recv()

    async def download(self, query: str) -> list[tuple[Song, Path | None]]:
        async with spotify_download_semaphore:
            return await asyncio.to_thread(self._download, query)
