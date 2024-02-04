import pandas as pd

def filter_unique_songs(initial_dataset, user_playlist):
    initial_songs_set = {(song["Name"], song["Artist"]) for song in initial_dataset}
    unique_songs_in_playlist = []
    for song in user_playlist:
        if (song["Name"], song["Artist"]) not in initial_songs_set:
            unique_songs_in_playlist.append(song)
    if unique_songs_in_playlist:
        print("Unique songs in user playlist:")
        for song in unique_songs_in_playlist:
            print(f"{song['Name']} by {song['Artist']}")
    else:
        print("No unique songs found in user playlist.")
    return unique_songs_in_playlist

