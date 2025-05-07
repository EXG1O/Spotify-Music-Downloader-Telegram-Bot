from spotdl import Song

from core.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

from .engine import Spotify

spotify = Spotify(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
)

__all__ = ['Spotify', 'Song']
