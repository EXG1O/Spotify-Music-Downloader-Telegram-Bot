from core.settings import TRACKS_PATH

from asyncio import Semaphore
from asyncio.subprocess import Process
from pathlib import Path
from tempfile import TemporaryDirectory
import asyncio
import os
import shutil


class Spotify:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

        self.semaphore = Semaphore(10)
        self.threads: int = max(1, (os.cpu_count() or 2) // 2)

    async def download(self, query: str) -> list[Path] | None:
        async with self.semaphore:
            with TemporaryDirectory(dir=TRACKS_PATH) as temp_dir:
                temp_path = Path(temp_dir)

                process: Process = await asyncio.create_subprocess_exec(
                    'spotdl',
                    '--client-id',
                    self.client_id,
                    '--client-secret',
                    self.client_secret,
                    '--threads',
                    str(self.threads),
                    '--bitrate',
                    '256k',
                    '--output',
                    str(temp_path),
                    '--log-format',
                    '[%(asctime)s]: %(levelname)s > %(process)d || %(message)s',
                    '--simple-tui',
                    query,
                )
                await process.wait()

                if process.returncode != 0:
                    return None

                temp_songs: list[Path] = list(temp_path.glob('*.mp3'))

                if not temp_songs:
                    return None

                final_songs: list[Path] = []

                for temp_song in temp_songs:
                    final_song: Path = TRACKS_PATH / temp_song.name

                    shutil.move(temp_song, final_song)
                    final_songs.append(final_song)

                return final_songs
