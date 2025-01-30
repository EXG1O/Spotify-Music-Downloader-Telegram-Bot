from spotdl import DownloaderOptions, Song
from spotdl.utils.search import parse_query
from spotdl.utils.spotify import SpotifyClient

from .downloader import Downloader

from pathlib import Path


class Spotify:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        settings: DownloaderOptions | None = None,
    ):
        SpotifyClient.init(
            client_id=client_id, client_secret=client_secret, no_cache=True
        )
        self.downloader = Downloader(settings)

    async def search(self, query: list[str]) -> list[Song]:
        return parse_query(
            query=query,
            threads=self.downloader.settings['threads'],
            use_ytm_data=self.downloader.settings['ytm_data'],
            playlist_numbering=self.downloader.settings['playlist_numbering'],
            album_type=self.downloader.settings['album_type'],
            playlist_retain_track_cover=self.downloader.settings[
                'playlist_retain_track_cover'
            ],
        )

    async def download(self, song: Song) -> tuple[Song, Path | None]:
        return await self.downloader.download_song(song)
