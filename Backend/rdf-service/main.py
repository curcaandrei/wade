from flask import Flask, request, redirect
import google_auth_oauthlib.flow
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from src import books, spotify
import os

load_dotenv()

app = Flask(__name__)


GOOGLE_BOOKS_REDIRECT_URI = os.getenv('GOOGLE_BOOKS_REDIRECT_URI')
GOOGLE_BOOKS_SCOPES = ['https://www.googleapis.com/auth/books']

flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    "google_client_secrets.json",
    scopes=GOOGLE_BOOKS_SCOPES,
    redirect_uri=GOOGLE_BOOKS_REDIRECT_URI
)
flow.redirect_uri = GOOGLE_BOOKS_REDIRECT_URI


SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
SPOTIFY_SCOPE = "user-library-read user-top-read user-read-recently-played"

sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SPOTIFY_SCOPE,
    show_dialog=True
)

# Routes for Google Books OAuth
@app.route('/callback/googlebooks')
def google_books_callback():
    code = request.args.get('code')
    flow.fetch_token(code=code)
    credentials = flow.credentials
    return books.fetch_data(credentials)

# Routes for Spotify OAuth
@app.route('/callback/spotify')
def spotify_callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    return spotify.fetch_data(token_info)

# Data fetching routes
@app.route('/spotify')
def get_spotify_data():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/books')
def get_books_data():
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
