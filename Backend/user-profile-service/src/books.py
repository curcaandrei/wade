import googleapiclient.discovery
import googleapiclient.errors


def fetch_data(credentials):
    try:
        books_service = googleapiclient.discovery.build('books', 'v1', credentials=credentials)

        bookshelves = books_service.mylibrary().bookshelves().list().execute()
        bookshelves_data = []

        for shelf in bookshelves.get('items', []):
            try:
                books = books_service.mylibrary().bookshelves().volumes().list(shelf=shelf['id']).execute()
            except googleapiclient.errors.HttpError:
                continue

            book_details = [get_book_info(book) for book in books.get('items', [])]
            shelf_info = {
                'id': shelf['id'],
                'title': shelf['title'],
                'books': book_details
            }
            bookshelves_data.append(shelf_info)

        return {'bookshelves': bookshelves_data}

    except Exception as e:
        return {'error': str(e)}

def get_book_info(book):
    info = book.get('volumeInfo', {})
    industry_identifiers = {identifier['type']: identifier['identifier'] for identifier in info.get('industryIdentifiers', [])}
    return {
        'Title': info.get('title', ''),
        'Authors': info.get('authors', []),
        'Description': info.get('description', ''),
        'Categories': info.get('categories', []),
        'AverageRating': info.get('averageRating'),
        'PreviewLink': info.get('previewLink'),
        'ISBN_10': industry_identifiers.get('ISBN_10'),
        'ISBN_13': industry_identifiers.get('ISBN_13'),
    }
