import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from dotenv import load_dotenv

load_dotenv()

REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

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
            get_liked_videos(credentials)

def get_liked_videos(credentials):
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials
    )
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        myRating="like"
    )
    response = request.execute()
    for item in response.get("items", []):
        print(item["snippet"]["title"])

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
