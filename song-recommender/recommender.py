from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

def run(user_json_data, vectorizer, initial_dataset_matrix,df_unique_tracks):

    user_df = pd.DataFrame(user_json_data)
    user_df['genres_artist'] = user_df['Genres'].apply(lambda x: ' '.join(x)) + ' ' + user_df['Artist']

    user_playlist_matrix = vectorizer.transform(user_df['genres_artist'])

    cosine_similarities = cosine_similarity(user_playlist_matrix, initial_dataset_matrix)
    top_two_song_indices = np.argsort(-cosine_similarities, axis=1)[:, :2]
    top_two_song_indices = np.argsort(-cosine_similarities, axis=1)[:, :2]
    recommended_songs = df_unique_tracks.iloc[top_two_song_indices.flatten()]
    recommendations = recommended_songs[['track_name', 'artist_name', 'album_name', 'uri', 'genres']]
    return recommendations.to_dict(orient='records')