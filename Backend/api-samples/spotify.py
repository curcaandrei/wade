from flask import Flask, request, redirect
import os
import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPE = "user-library-read user-top-read user-read-recently-played"

app = Flask(__name__)

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    show_dialog=True
)

@app.route('/')
def home():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    return get_user_data(token_info)

def get_user_data(token_info):
    if token_info:
        sp = spotipy.Spotify(auth=token_info['access_token'])

        # Retrieve favorite songs with more details
        top_tracks = sp.current_user_top_tracks(limit=50)
        favorite_songs = [{
            'Name': track['name'],
            'Artist': ", ".join([artist['name'] for artist in track['artists']]),
            'Album': track['album']['name'],
            'Genres': [genre for artist in track['artists'] for genre in sp.artist(artist['id'])['genres']]
        } for track in top_tracks['items']]

        # Retrieve artist details
        artist_ids = {artist['id'] for track in top_tracks['items'] for artist in track['artists']}
        artists_info = []
        for artist_id in artist_ids:
            artist_data = sp.artist(artist_id)
            artists_info.append({
                'Name': artist_data['name'],
                'Genres': artist_data['genres'],
                'Popularity': artist_data['popularity'],
                'Followers': artist_data['followers']['total']
            })

        spotify_data = {
            'favorite_songs': favorite_songs,
            'artists_info': artists_info
        }

        with open('spotify_user_data.json', 'w', encoding='utf-8') as f:
            json.dump(spotify_data, f, ensure_ascii=False, indent=4)

        return 'Data has been saved to spotify_user_data.json'

if __name__ == '__main__':
    app.run(port=8888)
