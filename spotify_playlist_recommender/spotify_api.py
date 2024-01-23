import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotipy_client = None


def authenticate_spotify(client_id, client_secret):
    credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

    global spotipy_client
    spotipy_client = spotipy.Spotify(client_credentials_manager=credentials)


# TODO: print this before prompting for playlist IDs
def get_user_playlists(user_id):
    return spotipy_client.user_playlists(user_id)


def get_playlist_tracks(playlist_id):
    results = spotipy_client.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = spotipy_client.next(results)
        tracks.extend(results['items'])
    return [track['track'] for track in tracks]


def get_playlist_details(playlist_id):
    return spotipy_client.playlist(playlist_id)
