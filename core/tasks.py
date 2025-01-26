from .settings import TRACKS_PATH

from pathlib import Path
import asyncio
import os
import time


async def check_downloaded_track_ages() -> None:
    while True:
        for track in os.listdir(TRACKS_PATH):
            track_path: Path = TRACKS_PATH / track
            track_age: float = time.time() - os.path.getatime(track_path)

            if track_age > 604800:
                os.remove(track_path)

        await asyncio.sleep(3600)


async def run_tasks() -> None:
    asyncio.create_task(check_downloaded_track_ages())
