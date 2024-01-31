import json
import mysql.connector
from mysql.connector import Error


config = {
        'user': 'root',
        'password': 'secret',
        'host':'localhost',
        'port': '3306',
        'database': 'users'
    }

def get_db_connection():
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def read_json(filename):
    with open(filename, 'r',encoding='utf-8') as file:
        data = json.load(file)
    return data

# Function to insert data into the books table
def insert_books(connection, books_data):
    try:
        cursor = connection.cursor()

        for book in books_data:
            if book['book_id']=='' or book['title']=='' or book['average_rating']=='' or book['image_url']=='':
                continue
            book_id = int(book['book_id'])
            average_rating=float(book['average_rating'])
            cursor.execute("INSERT INTO books (book_id, title, average_rating, image_url) VALUES (%s, %s, %s, %s)",
                           (book_id, book['title'], average_rating, book['image_url']))
        connection.commit()
        cursor.close()
        print("Books data inserted successfully")
    except Error as e:
        print("Error inserting data into books table:", e)

def insert_authors(connection, authors_data):
    try:
        cursor = connection.cursor()
        for author in authors_data:
            if author['author_id']=='' or author['name']=='':
                continue
            author_id = int(author['author_id'])  # Convert string ID to integer
            cursor.execute("INSERT INTO authors (author_id, name) VALUES (%s, %s)",
                           (author_id, author['name']))
        connection.commit()
        cursor.close()
        print("Authors data inserted successfully")
    except Error as e:
        print("Error inserting data into authors table:", e)

# Function to insert data into the user_book_interaction table
def insert_auth_book(connection, auth_book_data):
    try:
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        for interaction in auth_book_data:
            if interaction['book_id']=='' or interaction['author_id']=='':
                continue
            book_id = int(interaction['book_id'])
            author_id = int(interaction['author_id'])
            cursor.execute("INSERT INTO book_author (book_id, author_id) VALUES ( %s, %s)",
                           ( book_id, author_id))
        connection.commit()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        cursor.close()
        print("Book-author data inserted successfully")
    except Error as e:
        print("Error inserting data into book_author table:", e)

# Function to insert data into the similar_books table
def insert_similar_books(connection, similar_books_data):
    try:
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        for similar_book in similar_books_data:
            if similar_book['book_id']=='' or similar_book['similar_book_id']=='':
                continue
            book_id = int(similar_book['book_id'])
            similar_book_id = int(similar_book['similar_book_id'])
            cursor.execute("INSERT INTO similar_books (book_id, similar_book_id) VALUES (%s, %s)",
                           (book_id, similar_book_id))
        connection.commit()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        cursor.close()
        print("Similar books data inserted successfully")
    except Error as e:
        print("Error inserting data into similar_books table:", e)

def insert_user_interactions(connection, user_interaction_data):
    try:
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        for interaction in user_interaction_data:
            user_id=interaction['user_id']
            book_id = int(interaction['book_id'])
            rating=float(interaction['rating'])
            cursor.execute("INSERT INTO user_book_interaction (user_id, book_id,rating) VALUES (%s, %s, %s)",
                           (user_id,book_id,rating))
        connection.commit()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        cursor.close()
        print("Similar books data inserted successfully")
    except Error as e:
        print("Error inserting data into similar_books table:", e)

def main():
    #books_data = read_json('../resources/books.json')
    #authors_data = read_json('../resources/authors.json')
    #authors_books = read_json('../resources/auth-book.json')
    #similar_books_data = read_json('../resources/similar_books.json')


    user_book_interaction_data = read_json('../resources/user_interactions.json')
    connection = get_db_connection()

    if connection:
        #insert_books(connection, books_data)
        #insert_authors(connection, authors_data)
        #insert_auth_book(connection,authors_books)
        #insert_similar_books(connection,similar_books_data)
        insert_user_interactions(connection,user_book_interaction_data)
        connection.close()

main()