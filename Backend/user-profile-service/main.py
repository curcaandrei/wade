import json
import tempfile
import praw
from flask import Flask, request, redirect
import google_auth_oauthlib.flow
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from google.cloud import secretmanager
from src import books, spotify, youtube
from flask import Flask,request
import sys
sys.path.append('src')
import dockerdb
from src.populatedb import populate
from flask_cors import CORS


# Load environment variables
load_dotenv()

# Flask application

app = Flask(__name__)
CORS(app)

# Constants
PROJECT_ID = "diesel-nova-412314"
SCOPES = {
    'google_books': ['https://www.googleapis.com/auth/books'],
    'youtube': ["https://www.googleapis.com/auth/youtube.readonly"],
    'spotify': "user-library-read user-top-read user-read-recently-played",
    'reddit': ['mysubreddits', 'read']
}

#Initialize secret manager client
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

app.secret_key = access_secret_version("APP_SECRET")
#Routes for each service
@app.route('/callback/googlebooks')
def google_books_callback():
    user_id = request.args.get('state')
    code = request.args.get('code')
    flow_google_books.fetch_token(code=code)
    credentials = flow_google_books.credentials
    data = books.fetch_data(credentials)
    dockerdb.save_api_data("google_books", user_id, json.dumps(data))
    return data

@app.route('/callback/youtube')
def youtube_callback():
    user_id = request.args.get('state')
    code = request.args.get('code')
    flow_youtube.fetch_token(code=code)
    credentials = flow_youtube.credentials
    data = youtube.fetch_data(credentials)
    dockerdb.save_api_data("youtube", user_id, json.dumps(data))
    return data

@app.route('/callback/spotify')
def spotify_callback():
    user_id = request.args.get('state')
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    data = spotify.fetch_data(token_info)
    dockerdb.save_api_data("spotify", user_id, json.dumps(data))
    return data

@app.route('/callback/reddit')
def reddit_callback():
    user_id = request.args.get('state')
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
    dockerdb.save_api_data("reddit", user_id, json.dumps(data))
    return data

@app.route('/spotify')
def get_spotify_data():
    user_id = request.args.get('user_id')
    auth_url = sp_oauth.get_authorize_url(state=user_id)
    return redirect(auth_url)

@app.route('/books')
def get_books_data():
    user_id = request.args.get('user_id')
    auth_url, _ = flow_google_books.authorization_url(prompt='consent', state=user_id)
    return redirect(auth_url)

@app.route('/youtube')
def get_youtube_data():
    user_id = request.args.get('user_id')
    auth_url, _ = flow_youtube.authorization_url(prompt='consent', state=user_id)
    return redirect(auth_url)

@app.route('/reddit')
def get_reddit_data():
    user_id = request.args.get('user_id')
    auth_url = reddit.auth.url(scopes=SCOPES['reddit'], state=user_id, duration='permanent')
    return redirect(auth_url)

@app.route('/data' , methods=['POST'])
def populatedb():
   return populate()

@app.route('/users', methods=['GET'])
def get_users():
    return dockerdb.get_users()

@app.route('/users-filter', methods=['GET'])
def get_filtered_users():
    city = request.args.get('city')
    company = request.args.get('company')
    skill= request.args.get('skill')
    return dockerdb.get_filtered_users(city,company,skill)

@app.route('/users', methods=['POST'])
def add_user():
    data=request.get_json()
    return dockerdb.add_user(data)
"""
Retrieve cities, companies, skilss using this method
"""
@app.route('/users/resources/<resource>', methods=['GET'])
def get_users_resources(resource):
    limit = request.args.get('limit')
    return dockerdb.get_users_resources(resource,limit)

@app.route('/users/check-user', methods=['POST'])
def check_user():
    data = request.json
    return dockerdb.check_user(data)

@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    return dockerdb.get_user(user_id)
@app.route('/users/<string:user_id>', methods=['PATCH'])
def update_user(user_id):
    data = request.json
    return dockerdb.update_user(user_id,data)

@app.route('/books', methods=['GET'])
def get_books():
    page = int(request.args.get('startId', 1))
    per_page = int(request.args.get('limit', 10))
    return dockerdb.get_books(page, per_page)

@app.route('/users/spotify/<string:user_id>',  methods=['GET'])
def get_spotify_data_for_user(user_id):
    data = dockerdb.get_apidata_for_user_from_table(user_id,'spotify')
    return data
@app.route('/users/mapping/<string:user_id>')
def get_long_id_of_user(user_id):
    data = dockerdb.get_mapper_id_of_user(user_id)
    return data

@app.route('/users/interactions/<user_id>', methods=['GET'])
def check_user_interactions(user_id):
    return dockerdb.check_user_interaction(user_id)

@app.route('/users/random-books', methods=['GET'])
def get_list_of_random_books():
    return dockerdb.get_random_books_with_ids()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
