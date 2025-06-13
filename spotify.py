import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from random import randint
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

JOY_PLAYLIST1 = "spotify:playlist:7GhawGpb43Ctkq3PRP1fOL"
JOY_PLAYLIST2 = "spotify:playlist:4Fh0313D3PitYzICKHhZ7r"

def create_spotify_client_creds():
    return SpotifyClientCredentials(
                        client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET)

def retrieve_playlist_tracks(pl):
    sp_client_creds = create_spotify_client_creds()
    sp = spotipy.Spotify(auth_manager=sp_client_creds)

    playlist_data = sp.playlist(pl)
    return playlist_data['tracks']['items']

def generate_random_track(pl):
    return pl[randint(0, len(pl))]['track']

def get_track_name(track):
    return track['name']

def get_track_url(track):
    return track['external_urls']['spotify']

def get_track_pic(track):
    return track['album']['images'][1]['url']

def get_artist(track):
    return track["artists"][0]["name"]

