import os
import spotipy
import webbrowser
import pandas as pd
from spotipy import CacheHandler
from spotipy.oauth2 import SpotifyOAuth
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

scope = "user-library-read user-top-read user-read-recently-played"

token_info = None

class NoCacheHandler(CacheHandler):
    def get_cached_token(self):
        return None

    def save_token_to_cache(self, token_info):
        pass

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope,
    cache_path=None,
    cache_handler=NoCacheHandler(),
    show_dialog=True
)

# Handler for callback - If user accesses localhost:8888/callback?code=.... Get the code
class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global token_info
        if self.path.startswith("/callback"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"You can close this window now.")
            code = self.path.split('?code=')[1]
            token_info = sp_oauth.get_access_token(code)

# Start local server
def start_server():
    server = HTTPServer(('localhost', 8888), OAuthHandler)
    server.handle_request()

# Function to get the authorization URL where the user can agree to provide access
def get_auth_url():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

# Function to get user data
def get_user_data():
    if token_info:
        sp = spotipy.Spotify(auth=token_info['access_token'])

        top_tracks = sp.current_user_top_tracks()
        favorite_songs = [{
            'Name': track['name'],
            'Artist': ", ".join([artist['name'] for artist in track['artists']]),
            'Album': track['album']['name']
        } for track in top_tracks['items']]
        df_favorites = pd.DataFrame(favorite_songs)

        recently_played = sp.current_user_recently_played()
        last_played = [{
            'Name': item['track']['name'],
            'Artist': ", ".join([artist['name'] for artist in item['track']['artists']]),
            'Played At': item['played_at']
        } for item in recently_played['items']]
        df_last_played = pd.DataFrame(last_played)

        artist_list = []
        genre_list = []
        for track in top_tracks['items']:
            for artist in track['artists']:
                artist_data = sp.artist(artist['id'])
                artist_list.append({
                    'Artist Name': artist_data['name'],
                    'Artist Genres': ", ".join(artist_data['genres']),
                    'Artist Popularity': artist_data['popularity']
                })
                genre_list.extend(artist_data['genres'])

        df_artists = pd.DataFrame(artist_list).drop_duplicates()
        df_genres = pd.DataFrame(list(set(genre_list)), columns=['Genre'])

        with pd.ExcelWriter('spotify_favorites.xlsx') as writer:
            df_favorites.to_excel(writer, sheet_name='Favorite Songs', index=False)
            df_last_played.to_excel(writer, sheet_name='Last Played', index=False)
            df_artists.to_excel(writer, sheet_name='Artists', index=False)
            df_genres.to_excel(writer, sheet_name='Genres', index=False)

        print("Data has been written to spotify_favorites.xlsx")

# Start the server in a new thread
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Open the authorization URL in the user's browser
auth_url = get_auth_url()
webbrowser.open(auth_url)

# The script will pause here until the server handles a single request
server_thread.join()

# Once the user has authorized and the code has been received, we can get the user data
get_user_data()
