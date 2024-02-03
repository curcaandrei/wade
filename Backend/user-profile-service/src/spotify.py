import spotipy
from dotenv import load_dotenv

load_dotenv()

def fetch_data(token_info):
    if token_info:
        sp = spotipy.Spotify(auth=token_info['access_token'])

        # Retrieve favorite songs with more details
        top_tracks = sp.current_user_top_tracks(limit=50)
        favorite_songs = [{
            'Name': track['name'],
            'Artist': ", ".join([artist['name'] for artist in track['artists']]),
            'Album': track['album']['name'],
            'Genres': [genre for artist in track['artists'] for genre in sp.artist(artist['id'])['genres']]
        } for track in top_tracks['items']]

        # Retrieve artist details
        artist_ids = {artist['id'] for track in top_tracks['items'] for artist in track['artists']}
        artists_info = []
        for artist_id in artist_ids:
            artist_data = sp.artist(artist_id)
            artists_info.append({
                'Name': artist_data['name'],
                'Genres': artist_data['genres'],
                'Popularity': artist_data['popularity'],
                'Followers': artist_data['followers']['total']
            })

        spotify_data = {
            'favorite_songs': favorite_songs,
            'artists_info': artists_info
        }

        return spotify_data
