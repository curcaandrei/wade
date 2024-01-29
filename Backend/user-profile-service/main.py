import json
import tempfile
import praw
from flask import Flask, request, redirect
import google_auth_oauthlib.flow
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from google.cloud import secretmanager
from src import books, spotify, youtube, database

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
@app.route('/callback/googlebooks/<user_id>')
def google_books_callback(user_id):
    code = request.args.get('code')
    flow_google_books.fetch_token(code=code)
    credentials = flow_google_books.credentials
    data = books.fetch_data(credentials)
    database.save_api_data("books", user_id, json.dumps(data))
    return data

@app.route('/callback/youtube/<user_id>')
def youtube_callback(user_id):
    code = request.args.get('code')
    flow_youtube.fetch_token(code=code)
    credentials = flow_youtube.credentials
    data = youtube.fetch_data(credentials)
    database.save_api_data("youtube", user_id, json.dumps(data))
    return data

@app.route('/callback/spotify/<user_id>')
def spotify_callback(user_id):
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    data = spotify.fetch_data(token_info)
    database.save_api_data("spotify", user_id, json.dumps(data))
    return data

@app.route('/callback/reddit/<user_id>')
def reddit_callback(user_id):
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

    data = {
        'subscribed_subreddits': subscribed_subreddits
    }
    database.save_api_data("reddit", user_id, json.dumps(data))
    return data

@app.route('/spotify')
def get_spotify_data():
    user_id = request.args.get('user_id')
    auth_url = sp_oauth.get_authorize_url()
    auth_url_with_user_id = f"{auth_url}&state={user_id}"
    return redirect(auth_url_with_user_id)

@app.route('/books')
def get_books_data():
    user_id = request.args.get('user_id')
    auth_url, _ = flow_google_books.authorization_url(prompt='consent')
    auth_url_with_user_id = f"{auth_url}&state={user_id}"
    return redirect(auth_url_with_user_id)

@app.route('/youtube')
def get_youtube_data():
    user_id = request.args.get('user_id')
    auth_url, _ = flow_youtube.authorization_url(prompt='consent')
    auth_url_with_user_id = f"{auth_url}&state={user_id}"
    return redirect(auth_url_with_user_id)

@app.route('/reddit')
def get_reddit_data():
    user_id = request.args.get('user_id')
    auth_url = reddit.auth.url(scopes=SCOPES['reddit'], state=user_id, duration='permanent')  # Pass user_id as state
    return redirect(auth_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
