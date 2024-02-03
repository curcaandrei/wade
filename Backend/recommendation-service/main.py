from flask import Flask, request, jsonify
import requests
from src.books import form_sparql_query_books, process_rdf_data_books
from src.movies import form_sparql_query_movies, process_rdf_data_movies
from src.music import form_sparql_query_music, process_rdf_data_music

app = Flask(__name__)

@app.route('/recommendations/books', methods=['POST'])
def get_book_recommendations():
    return get_recommendations(form_sparql_query_books, process_rdf_data_books)

@app.route('/recommendations/movies', methods=['POST'])
def get_movie_recommendations():
    return get_recommendations(form_sparql_query_movies, process_rdf_data_movies)

@app.route('/recommendations/music', methods=['POST'])
def get_music_recommendations():
    return get_recommendations(form_sparql_query_music, process_rdf_data_music)

def get_recommendations(form_sparql_query, process_rdf_data):
    data = request.json
    sparql_query = form_sparql_query(data)
    response = requests.post('https://rdf-dot-diesel-nova-412314.ew.r.appspot.com/query', json={'query': sparql_query})
    rdf_data = response.json()
    processed_data = process_rdf_data(rdf_data)
    return jsonify(processed_data)

if __name__ == '__main__':
    app.run(port=5000)
