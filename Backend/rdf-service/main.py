import praw
from flask import Flask, request, redirect
import google_auth_oauthlib.flow
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from src import books, spotify, youtube
from google.cloud import secretmanager
import tempfile

load_dotenv()

app = Flask(__name__)

project_id = "diesel-nova-412314"

def access_secret_version(project_id, secret_id, version_id="latest"):
    """
    Accesses the payload of the given secret version if it exists.

    :param project_id: Google Cloud project ID
    :param secret_id: ID of the secret to access
    :param version_id: version of the secret; defaults to "latest"
    :return: secret payload as a string 
    """
    client = secretmanager.SecretManagerServiceClient()

    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})

    # Return the decoded payload of the secret
    return response.payload.data.decode("UTF-8")


GOOGLE_BOOKS_REDIRECT_URI = access_secret_version(project_id, "GOOGLE_BOOKS_REDIRECT_URI")
GOOGLE_BOOKS_SCOPES = ['https://www.googleapis.com/auth/books']

YOUTUBE_BOOKS_REDIRECT_UI = access_secret_version(project_id, "YOUTUBE_REDIRECT_URI")
YOUTUBE_SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
]

google_client_secrets_content = access_secret_version(project_id, "GOOGLE_CLIENT_SECRETS")
with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
    temp_file.write(google_client_secrets_content)
    temp_file_path = temp_file.name

flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    temp_file_path,
    scopes=GOOGLE_BOOKS_SCOPES,
    redirect_uri=GOOGLE_BOOKS_REDIRECT_URI
)
flow.redirect_uri = GOOGLE_BOOKS_REDIRECT_URI

youtubeflow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    temp_file_path,
    scopes=YOUTUBE_SCOPES,
    redirect_uri=YOUTUBE_BOOKS_REDIRECT_UI
)
youtubeflow.redirect_uri = YOUTUBE_BOOKS_REDIRECT_UI

SPOTIFY_CLIENT_ID = access_secret_version(project_id, "SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = access_secret_version(project_id, "SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = access_secret_version(project_id, "SPOTIFY_REDIRECT_URI")
SPOTIFY_SCOPE = "user-library-read user-top-read user-read-recently-played"

sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SPOTIFY_SCOPE,
    show_dialog=True
)

REDDIT_CLIENT_ID = access_secret_version(project_id, "REDDIT_ID")
REDDIT_CLIENT_SECRET = access_secret_version(project_id, "REDDIT_SECRET")
REDDIT_USER_AGENT = access_secret_version(project_id, "REDDIT_USER_AGENT")
REDDIT_REDIRECT_URI = access_secret_version(project_id, "REDDIT_REDIRECT_URI")

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     redirect_uri=REDDIT_USER_AGENT,
                     user_agent=REDDIT_REDIRECT_URI)


# Routes for Google Books OAuth
@app.route('/callback/googlebooks')
def google_books_callback():
    code = request.args.get('code')
    flow.fetch_token(code=code)
    credentials = flow.credentials
    return books.fetch_data(credentials)

# Routes for Google Books OAuth
@app.route('/callback/youtube')
def youtube_callback():
    code = request.args.get('code')
    youtubeflow.fetch_token(code=code)
    credentials = youtubeflow.credentials
    return youtube.fetch_data(credentials)

# Routes for Spotify OAuth
@app.route('/callback/spotify')
def spotify_callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    return spotify.fetch_data(token_info)

@app.route('/callback/reddit')
def callback():
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

# Data fetching routes
@app.route('/spotify')
def get_spotify_data():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/books')
def get_books_data():
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)

@app.route('/youtube')
def home():
    auth_url, _ = youtubeflow.authorization_url(prompt='consent')
    return redirect(auth_url)

@app.route('/reddit')
def home():
    scope = ['mysubreddits', 'read']
    auth_url = reddit.auth.url(scopes=scope, state='...', duration='permanent')
    return redirect(auth_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
