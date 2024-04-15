import numpy as np
import pandas as pd
df = pd.read_csv('spotify-2023.csv', encoding="ISO-8859-1")
#Data Columns: ['track_name', 'artist(s)_name', 'artist_count', 'released_year',
       # 'released_month', 'released_day', 'in_spotify_playlists',
       # 'in_spotify_charts', 'streams', 'in_apple_playlists', 'in_apple_charts',
       # 'in_deezer_playlists', 'in_deezer_charts', 'in_shazam_charts', 'bpm',
       # 'key', 'mode', 'danceability_%', 'valence_%', 'energy_%',
       # 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%']

#Columns we will not consider: track name, key

#Create dictionary of artists
artist_dict = {}
artist_count = 0

artist_ids = []
mode_ids = []
for _, song in df.iterrows():
    artist = song["artist(s)_name"].split(',')[0]
    artist = artist.strip()
    if artist not in artist_dict:
        artist_dict[artist] = artist_count
        artist_count += 1
    artist_id = artist_dict[artist]
    artist_ids.append(artist_id)
    if song['mode'] == 'major':
        mode_ids.append(1)
    else:
        mode_ids.append(0)

df["artist_ids"] = artist_ids
df["mode_ids"] = mode_ids

selected_columns = ['artist_ids', 'released_year', 'in_spotify_playlists',
                    'in_spotify_charts', 'streams', 'in_apple_playlists',
                    'in_apple_charts', 'in_deezer_playlists', 'in_deezer_charts',
                    'in_shazam_charts', 'bpm', 'mode_ids', 'danceability_%',
                    'valence_%', 'energy_%', 'acousticness_%',
                         'instrumentalness_%', 'liveness_%', 'speechiness_%']

songs_array = df[selected_columns].values

track_names_array = df['track_name'].values
track_name_to_index = {}
track_index_to_name = {}

valid_rows = []
# Iterate over each row
for row_index in range(songs_array.shape[0]):
    valid_row = True
    # Iterate over each column
    for col_index in range( songs_array.shape[1]):
        try:
            # Try to convert the value to int
            int(songs_array[row_index, col_index])
        except ValueError:
            # If ValueError occurs, mark row as invalid and break
            valid_row = False
            break
    # If all columns in the row are convertible to int, mark row as valid
    if valid_row:
        valid_rows.append(row_index)


# Filter the array to keep only valid rows
songs_array = songs_array[valid_rows, :]
track_names_array = track_names_array[valid_rows]
for idx, name in enumerate(track_names_array):
    track_name_to_index[name] = idx
    track_index_to_name[idx] = name

songs_array = songs_array.astype(int)
U, _, _ = np.linalg.svd(songs_array)

def get_k_most_similar(song_name, k):
    similarity_scores = []
    song_idx = track_name_to_index[song_name]
    song_u = U[song_idx]
    for idx, candidate_u in enumerate(U):
        if idx == song_idx:
            continue
        candidate_name = track_index_to_name[idx]
        similarity_scores.append((candidate_name, np.dot(song_u, candidate_u)))
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1])
    return [pair[0] for pair in sorted_scores[:3]]

print(track_names_array[5])
print(get_k_most_similar(track_names_array[5], 3))
    
# print("U:\n", U)
# print(np.dot(U[0], U[2]))
# print("S:\n", S)
# print("V:\n", V)
