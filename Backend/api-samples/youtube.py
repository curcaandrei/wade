from flask import Flask, request, redirect
import google_auth_oauthlib.flow
import googleapiclient.discovery
import os
import json
from dotenv import load_dotenv

load_dotenv()

REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
]

app = Flask(__name__)

flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    "google_client_secrets.json",
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI
)
flow.redirect_uri = REDIRECT_URI

@app.route('/')
def home():
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    flow.fetch_token(code=code)
    credentials = flow.credentials
    return get_user_data(credentials)

def get_user_data(credentials):
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials
    )

    # Fetch liked videos with tags and descriptions
    liked_videos_request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        myRating="like"
    )
    liked_videos_response = liked_videos_request.execute()
    liked_videos_data = [{
        'Title': item['snippet']['title'],
        'Video ID': item['id'],
        'Published At': item['snippet']['publishedAt'],
        'Tags': item['snippet'].get('tags', []),
        'Description': item['snippet'].get('description', '')
    } for item in liked_videos_response.get("items", [])]

    # Fetch subscribed channels with descriptions
    subscriptions_request = youtube.subscriptions().list(
        part="snippet,contentDetails",
        mine=True,
        maxResults=50
    )
    subscriptions_response = subscriptions_request.execute()
    subscribed_channels_data = []
    for item in subscriptions_response.get("items", []):
        channel_id = item['snippet']['resourceId']['channelId']
        channel_data = youtube.channels().list(
            part="snippet,brandingSettings",
            id=channel_id
        ).execute()

        if channel_data['items']:
            channel_info = channel_data['items'][0]
            channel_details = {
                'Channel Title': channel_info['snippet']['title'],
                'Channel ID': channel_id,
                'Description': channel_info['snippet'].get('description', ''),
                'Keywords': channel_info['brandingSettings']['channel'].get('keywords', '')
            }
            subscribed_channels_data.append(channel_details)

    youtube_data = {
        'liked_videos': liked_videos_data,
        'subscribed_channels': subscribed_channels_data
    }

    with open('youtube_user_data.json', 'w', encoding='utf-8') as f:
        json.dump(youtube_data, f, ensure_ascii=False, indent=4)

    return 'Data has been saved to youtube_user_data.json'

if __name__ == '__main__':
    app.run(port=8888)
