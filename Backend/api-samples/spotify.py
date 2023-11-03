import os
import spotipy
import webbrowser

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
        results = sp.current_user_top_tracks()  # This gets the top tracks of the user
        for track in results['items']:
            print(track['name'])
    else:
        print("Can't get token for user")

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
