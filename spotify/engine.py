from spotdl.types.song import Song

from .utils import spotdl_client

from asyncio import Semaphore
from pathlib import Path
import asyncio


class Spotify:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

        self.semaphore = Semaphore(10)

    def _download(self, query: str) -> list[tuple[Song, Path | None]]:
        with spotdl_client(self.client_id, self.client_secret) as spotdl:
            songs: list[Song] = spotdl.search([query])
            return spotdl.download_songs(songs)

    async def download(self, query: str) -> list[tuple[Song, Path | None]]:
        async with self.semaphore:
            return await asyncio.to_thread(self._download, query)
