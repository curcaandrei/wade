from flask import Flask, request, redirect
import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv

load_dotenv()

REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPES = ['https://www.googleapis.com/auth/books']

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
    books_service = googleapiclient.discovery.build('books', 'v1', credentials=credentials)

    bookshelves = books_service.mylibrary().bookshelves().list().execute()
    bookshelves_data = []

    for shelf in bookshelves.get('items', []):
        try:
            books = books_service.mylibrary().bookshelves().volumes().list(shelf=shelf['id']).execute()
        except googleapiclient.errors.HttpError:
            # Skip the bookshelf if there's an HTTP error (e.g., not found)
            continue

        book_details = []
        for book in books.get('items', []):
            info = book.get('volumeInfo', {})
            book_info = {
                'Title': info.get('title', ''),
                'Authors': info.get('authors', []),
                'Description': info.get('description', ''),
                'Categories': info.get('categories', [])
            }
            book_details.append(book_info)

        shelf_info = {
            'id': shelf['id'],
            'title': shelf['title'],
            'books': book_details
        }
        bookshelves_data.append(shelf_info)

    google_books_data = {
        'bookshelves': bookshelves_data
    }

    with open('google_books_user_data.json', 'w', encoding='utf-8') as f:
        json.dump(google_books_data, f, ensure_ascii=False, indent=4)

    return 'Data has been saved to google_books_user_data.json'

if __name__ == '__main__':
    app.run(port=8888)
