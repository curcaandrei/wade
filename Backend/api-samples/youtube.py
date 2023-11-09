import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from dotenv import load_dotenv
import pandas as pd
import rdflib
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF

# RDF
g = rdflib.Graph()

YOUTUBE = rdflib.Namespace("http://www.youtube.com/")
g.bind("youtube", YOUTUBE)

load_dotenv()

REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.channel-memberships.creator",
    "https://www.googleapis.com/auth/youtubepartner",
]

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query_s = self.path.split('?', 1)[-1]
        query = dict(qc.split('=') for qc in query_s.split('&'))
        if 'code' in query:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"You can close this window now.")
            flow.fetch_token(code=query['code'])
            credentials = flow.credentials
            get_user_data(credentials)

def get_user_data(credentials):
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials
    )
    with pd.ExcelWriter('youtube_data.xlsx', engine='openpyxl') as writer:

        # Fetch liked videos
        liked_videos_request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            myRating="like"
        )
        liked_videos_response = liked_videos_request.execute()
        liked_videos_data = [{
            'Title': item['snippet']['title'],
            'Video ID': item['id'],
            'Published At': item['snippet']['publishedAt']
        } for item in liked_videos_response.get("items", [])]
        df_liked_videos = pd.DataFrame(liked_videos_data)
        df_liked_videos.to_excel(writer, sheet_name='Liked Videos', index=False)

        # Fetch subscribed channels
        subscriptions_request = youtube.subscriptions().list(
            part="snippet,contentDetails",
            mine=True,
            maxResults=50
        )
        subscriptions_response = subscriptions_request.execute()
        subscribed_channels_data = [{
            'Channel Title': item['snippet']['title'],
            'Channel ID': item['snippet']['resourceId']['channelId']
        } for item in subscriptions_response.get("items", [])]
        df_subscribed_channels = pd.DataFrame(subscribed_channels_data)
        df_subscribed_channels.to_excel(writer, sheet_name='Subscribed Channels', index=False)

        for video in liked_videos_data:
            video_uri = URIRef(f"http://www.youtube.com/video/{video['Video ID']}")
            g.add((video_uri, RDF.type, YOUTUBE.Video))
            g.add((video_uri, FOAF.name, Literal(video['Title'])))
            g.add((video_uri, YOUTUBE.publishedAt, Literal(video['Published At'])))

        for channel in subscribed_channels_data:
            channel_uri = URIRef(f"http://www.youtube.com/channel/{channel['Channel ID']}")
            g.add((channel_uri, RDF.type, YOUTUBE.Channel))
            g.add((channel_uri, FOAF.name, Literal(channel['Channel Title'])))


        writer.save()

def start_server():
    server = HTTPServer(('localhost', 8888), OAuthHandler)
    server.handle_request()

# Disable OAuthlib's HTTPS verification when running locally
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    "youtube_client_secrets.json",
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI
)

flow.redirect_uri = REDIRECT_URI

auth_url, _ = flow.authorization_url(prompt='consent')

server_thread = threading.Thread(target=start_server)
server_thread.start()

webbrowser.open(auth_url)

server_thread.join()


turtle_data = g.serialize(format='turtle')

print(turtle_data)

with open("youtube_data.ttl", "w") as f:
    f.write(turtle_data)
