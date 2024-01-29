import tempfile
import praw
from flask import Flask, request, redirect
import google_auth_oauthlib.flow
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from google.cloud import secretmanager
from src import books, spotify, youtube

# Load environment variables
load_dotenv()

# Flask application
app = Flask(__name__)

# Constants
PROJECT_ID = "diesel-nova-412314"
SCOPES = {
    'google_books': ['https://www.googleapis.com/auth/books'],
    'youtube': ["https://www.googleapis.com/auth/youtube.readonly"],
    'spotify': "user-library-read user-top-read user-read-recently-played",
    'reddit': ['mysubreddits', 'read']
}

# Initialize secret manager client
secret_client = secretmanager.SecretManagerServiceClient()

def access_secret_version(secret_id, version_id="latest"):
    """
    Accesses the payload of the given secret version if it exists.
    """
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    response = secret_client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Initialize OAuth flows
def init_google_flow(scopes, redirect_uri_key):
    client_secrets_content = access_secret_version("GOOGLE_CLIENT_SECRETS")
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_file.write(client_secrets_content)
        temp_file_path = temp_file.name

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        temp_file_path,
        scopes=scopes,
        redirect_uri=access_secret_version(redirect_uri_key)
    )
    return flow

flow_google_books = init_google_flow(SCOPES['google_books'], "GOOGLE_BOOKS_REDIRECT_URI")
flow_youtube = init_google_flow(SCOPES['youtube'], "YOUTUBE_REDIRECT_URI")

sp_oauth = SpotifyOAuth(
    client_id=access_secret_version("SPOTIFY_CLIENT_ID"),
    client_secret=access_secret_version("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=access_secret_version("SPOTIFY_REDIRECT_URI"),
    scope=SCOPES['spotify'],
    show_dialog=True
)

reddit = praw.Reddit(
    client_id=access_secret_version("REDDIT_ID"),
    client_secret=access_secret_version("REDDIT_SECRET"),
    redirect_uri=access_secret_version("REDDIT_REDIRECT_URI"),
    user_agent=access_secret_version("REDDIT_USER_AGENT")
)

# Routes for each service
@app.route('/callback/googlebooks')
def google_books_callback():
    code = request.args.get('code')
    flow_google_books.fetch_token(code=code)
    credentials = flow_google_books.credentials
    return books.fetch_data(credentials)

@app.route('/callback/youtube')
def youtube_callback():
    code = request.args.get('code')
    flow_youtube.fetch_token(code=code)
    credentials = flow_youtube.credentials
    return youtube.fetch_data(credentials)

@app.route('/callback/spotify')
def spotify_callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    return spotify.fetch_data(token_info)

@app.route('/callback/reddit')
def reddit_callback():
    code = request.args.get('code')
    reddit.auth.authorize(code)

    subscribed_subreddits = []
    for subreddit in reddit.user.subreddits(limit=None):
        subreddit_info = {
            'name': subreddit.display_name,
            'description': subreddit.public_description,
            'subscribers': subreddit.subscribers,
            'top_posts': [{'title': post.title, 'url': post.url} for post in subreddit.top(limit=10)]
        }
        subscribed_subreddits.append(subreddit_info)

    user_data = {
        'subscribed_subreddits': subscribed_subreddits
    }
    return user_data

@app.route('/spotify')
def get_spotify_data():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/books')
def get_books_data():
    auth_url, _ = flow_google_books.authorization_url(prompt='consent')
    return redirect(auth_url)

@app.route('/youtube')
def get_youtube_data():
    auth_url, _ = flow_youtube.authorization_url(prompt='consent')
    return redirect(auth_url)

@app.route('/reddit')
def get_reddit_data():
    auth_url = reddit.auth.url(scopes=SCOPES['reddit'], state='...', duration='permanent')
    return redirect(auth_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
