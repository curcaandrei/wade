from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from simgleton import Singleton
from recommender import run
import random
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

user_pf_url = "http://127.0.0.1:5000/users/spotify/"
df_unique_tracks = Singleton().df
vectorizer = TfidfVectorizer()
df_unique_tracks.loc[:, 'genres_artist'] = df_unique_tracks['genres'] + ' ' + df_unique_tracks['artist_name']
initial_dataset_matrix = vectorizer.fit_transform(df_unique_tracks['genres_artist'])


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/song-recommender', methods=['GET'])
def recommend_songs():
    data = request.json
    data = process_data(data)
    data = process_request(data)
    return jsonify(run(data, vectorizer, initial_dataset_matrix, df_unique_tracks)), 200


@app.route('/song-recommender/<string:user_id>', methods=['GET'])
def recommend_songs_for_user(user_id):
    response = requests.get(user_pf_url + user_id)
    if response.status_code == 404:
        random_data = get_random_songs()
        return jsonify(run(random_data, vectorizer, initial_dataset_matrix, df_unique_tracks)), 200
    elif response.status_code == 200:
        data = response.json()['data']
        data = process_data(data)
        data = process_request(data)
        return jsonify(run(data, vectorizer, initial_dataset_matrix, df_unique_tracks)), 200
    else:
        print(f"Unexpected status code: {response.status_code}")
    return jsonify("Something unexpected occurred"), 500


def process_request(data: list):
    if len(data) > 5:
        num_elements = 5  # Choose a random number of elements
        return random.sample(data, num_elements)
    return data


def process_data(data):
    json_data = data['favorite_songs']
    return json_data

def  get_random_songs():
    n = 5
    random_sample = df_unique_tracks.sample(n)
    random_sample = random_sample.rename(columns={'artist_name': 'Artist', 'genres': 'Genres'})
    sample_list = random_sample.to_dict(orient='records')
    return sample_list
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8005)
